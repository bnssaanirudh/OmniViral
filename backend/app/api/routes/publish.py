"""Publish router: auto-publish optimized content to social platforms."""
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from backend.app.api.deps import DBSession, CurrentUser
from backend.app.models.asset import Asset
from backend.app.models.publication import Publication, Platform, PublicationStatus

router = APIRouter()


class PublishRequest(BaseModel):
    asset_id: uuid.UUID
    platforms: list[Platform] = [Platform.YOUTUBE]
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    scheduled_at: Optional[str] = None


class PublishResponse(BaseModel):
    publications: list[dict]
    total_published: int
    failures: list[str]


@router.post("/", response_model=PublishResponse)
async def publish_asset(
    request: PublishRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Publish an optimized asset to one or more social platforms.
    Uses mock API adapters by default; real adapters activated via env vars.
    """
    result = await db.execute(select(Asset).where(Asset.id == request.asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")

    publications = []
    failures = []

    for platform in request.platforms:
        try:
            pub_result = await _publish_to_platform(
                asset=asset,
                platform=platform,
                title=request.title or asset.title or asset.original_name,
                description=request.description or asset.description or "",
                tags=request.tags or [],
            )
            pub = Publication(
                asset_id=request.asset_id,
                platform=platform,
                status=PublicationStatus.PUBLISHED,
                title=pub_result["title"],
                description=pub_result["description"],
                platform_video_id=pub_result["video_id"],
                platform_url=pub_result["url"],
                virality_score_at_publish=pub_result.get("virality_score"),
                platform_response=pub_result,
                published_by=current_user.get("sub"),
            )
            db.add(pub)
            publications.append(pub_result)
        except Exception as e:
            failures.append(f"{platform}: {str(e)}")

    return PublishResponse(
        publications=publications,
        total_published=len(publications),
        failures=failures,
    )


async def _publish_to_platform(
    asset: Asset, platform: Platform, title: str, description: str, tags: list
) -> dict:
    """Route to the correct platform adapter."""
    from agents.publishing.publisher import get_publisher
    publisher = get_publisher(platform)
    return await publisher.publish(asset=asset, title=title, description=description, tags=tags)


@router.get("/", response_model=list[dict])
async def list_publications(db: DBSession, current_user: CurrentUser, page: int = 1):
    """List all publications."""
    result = await db.execute(
        select(Publication).order_by(Publication.created_at.desc()).offset((page - 1) * 20).limit(20)
    )
    pubs = result.scalars().all()
    return [
        {
            "id": str(p.id),
            "asset_id": str(p.asset_id),
            "platform": p.platform,
            "status": p.status,
            "platform_url": p.platform_url,
            "title": p.title,
            "views_count": p.views_count,
            "created_at": str(p.created_at),
        }
        for p in pubs
    ]


@router.get("/{pub_id}", response_model=dict)
async def get_publication(pub_id: uuid.UUID, db: DBSession, current_user: CurrentUser):
    """Get a specific publication."""
    result = await db.execute(select(Publication).where(Publication.id == pub_id))
    pub = result.scalar_one_or_none()
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found.")
    return {
        "id": str(pub.id),
        "asset_id": str(pub.asset_id),
        "platform": pub.platform,
        "status": pub.status,
        "title": pub.title,
        "platform_video_id": pub.platform_video_id,
        "platform_url": pub.platform_url,
        "virality_score_at_publish": pub.virality_score_at_publish,
        "views_count": pub.views_count,
        "likes_count": pub.likes_count,
        "comments_count": pub.comments_count,
        "watch_time_hours": pub.watch_time_hours,
        "platform_response": pub.platform_response,
        "created_at": str(pub.created_at),
    }
