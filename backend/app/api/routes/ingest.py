"""
Ingestion router: upload content assets and trigger processing pipeline.
"""
import uuid
import os
import aiofiles
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status, BackgroundTasks

from backend.app.api.deps import DBSession, CurrentUser
from backend.app.core.config import settings
from backend.app.models.asset import Asset, AssetStatus, AssetType
from backend.app.schemas.asset import AssetResponse, AssetListResponse
from sqlalchemy import select, func

router = APIRouter()

ALLOWED_EXTENSIONS = {
    "video": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    "script": [".txt", ".md", ".docx", ".pdf"],
    "image": [".jpg", ".jpeg", ".png", ".webp"],
    "audio": [".mp3", ".wav", ".m4a"],
    "metadata": [".json", ".yaml", ".yml", ".csv"],
}


def _detect_asset_type(filename: str) -> AssetType:
    ext = Path(filename).suffix.lower()
    for atype, exts in ALLOWED_EXTENSIONS.items():
        if ext in exts:
            return AssetType(atype)
    return AssetType.METADATA


async def _save_file(upload: UploadFile, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    size = 0
    async with aiofiles.open(dest, "wb") as f:
        while chunk := await upload.read(1024 * 1024):  # 1 MB chunks
            await f.write(chunk)
            size += len(chunk)
    return size


@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def ingest_asset(
    db: DBSession,
    current_user: CurrentUser,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str | None = Form(None),
    description: str | None = Form(None),
    category: str | None = Form(None),
    language: str | None = Form("en"),
    region: str | None = Form(None),
    platform: str | None = Form(None),
):
    """Upload and ingest a content asset. Triggers the full ML pipeline."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    asset_type = _detect_asset_type(file.filename)
    safe_name = f"{uuid.uuid4()}_{file.filename}"
    dest_path = Path(settings.LOCAL_STORAGE_PATH) / safe_name

    # Save file
    size = await _save_file(file, dest_path)

    # Create DB record
    asset = Asset(
        filename=safe_name,
        original_name=file.filename,
        asset_type=asset_type,
        status=AssetStatus.PENDING,
        title=title,
        description=description,
        category=category,
        language=language,
        region=region,
        platform=platform,
        file_size_bytes=size,
        storage_path=str(dest_path),
        tenant_id=current_user.get("sub"),
        uploaded_by=current_user.get("sub"),
    )
    db.add(asset)
    await db.flush()
    await db.refresh(asset)

    # Kick off pipeline in background
    background_tasks.add_task(_trigger_pipeline, str(asset.id))

    return asset


async def _trigger_pipeline(asset_id: str):
    """Trigger Celery pipeline (imported lazily to avoid circular deps)."""
    try:
        from backend.app.tasks.ingestion_tasks import process_asset
        process_asset.delay(asset_id)
    except Exception:
        pass  # Pipeline will be triggered by watchdog fallback


@router.get("/", response_model=AssetListResponse)
async def list_assets(
    db: DBSession,
    current_user: CurrentUser,
    page: int = 1,
    page_size: int = 20,
    status_filter: AssetStatus | None = None,
):
    """List all ingested assets with pagination."""
    offset = (page - 1) * page_size
    query = select(Asset)
    if status_filter:
        query = query.where(Asset.status == status_filter)
    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0
    result = await db.execute(query.offset(offset).limit(page_size))
    items = result.scalars().all()
    return AssetListResponse(items=list(items), total=total, page=page, page_size=page_size)


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: uuid.UUID, db: DBSession, current_user: CurrentUser):
    """Fetch a single asset by ID."""
    result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    return asset


@router.delete("/{asset_id}", status_code=204)
async def delete_asset(asset_id: uuid.UUID, db: DBSession, current_user: CurrentUser):
    """Delete an asset and its stored file."""
    result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    if asset.storage_path and os.path.exists(asset.storage_path):
        os.remove(asset.storage_path)
    await db.delete(asset)
