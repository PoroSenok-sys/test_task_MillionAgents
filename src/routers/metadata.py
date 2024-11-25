"""Роутер для работы с FileMetadata"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.db.models.metadata import FileMetadata

router = APIRouter(
    prefix="/metadata",
    tags=["Metadata"]
)


@router.get("/{file_id}")
async def get_metadata(file_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FileMetadata).where(FileMetadata.id == file_id))
    metadata = result.scalars().first()
    if not metadata:
        raise HTTPException(status_code=404, detail="File metadata not found")
    return metadata
