"""Функция для сохранения загружаемого файла"""
from pathlib import Path
from fastapi import UploadFile
from aiofiles import open as aio_open

from src.config import settings


async def save_file(file: UploadFile, uid: str) -> Path:
    filepath = Path(settings.LOCAL_STORAGE) / uid
    async with aio_open(filepath, "wb") as f:
        while chunk := await file.read(1024):
            await f.write(chunk)
    return filepath
