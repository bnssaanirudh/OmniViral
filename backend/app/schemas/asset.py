"""Pydantic schemas for Asset."""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from backend.app.models.asset import AssetType, AssetStatus


class AssetBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    region: Optional[str] = None
    platform: Optional[str] = None


class AssetCreate(AssetBase):
    original_name: str
    asset_type: AssetType
    file_size_bytes: Optional[int] = None
    duration_seconds: Optional[float] = None
    raw_metadata: Optional[dict] = None


class AssetUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[AssetStatus] = None
    features: Optional[dict] = None


class AssetResponse(AssetBase):
    id: uuid.UUID
    filename: str
    original_name: str
    asset_type: AssetType
    status: AssetStatus
    duration_seconds: Optional[float] = None
    file_size_bytes: Optional[int] = None
    storage_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AssetListResponse(BaseModel):
    items: list[AssetResponse]
    total: int
    page: int
    page_size: int
