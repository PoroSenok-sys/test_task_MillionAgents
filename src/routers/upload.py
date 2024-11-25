"""Роутер для загрузки файлов"""
import asyncio
import uuid
from fastapi import UploadFile, HTTPException, Depends, APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.services.savefile import save_file
from src.services.upload_to_cloud import upload_to_cloud
from src.db.models.metadata import FileMetadata

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_file(file: UploadFile, db: AsyncSession = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File must have a valid name")

    # Генерируем UID и сохраняем файл
    uid = str(uuid.uuid4())

    saved_path = await save_file(file, uid)

    # Достаем нужные метаданные
    file_size = saved_path.stat().st_size
    file_extension = saved_path.suffix
    file_format = file.content_type

    # Сохраняем метаданные в БД
    metadata = FileMetadata(
        id=uid,
        filename=file.filename,
        extension=file_extension,
        size=file_size,
        format=file_format
    )
    db.add(metadata)
    await db.commit()

    # Вызываем функцию загрузки в облако
    asyncio.create_task(upload_to_cloud(saved_path))

    return JSONResponse(content={
        "uid": uid, "massage": "Файл загружается в облако"})
