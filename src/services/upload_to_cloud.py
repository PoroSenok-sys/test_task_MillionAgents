"""Функция для загрузки файла в облако"""
import asyncio
from pathlib import Path

from src.config import settings


async def upload_to_cloud(file_path: Path):
    # Здесь будет логика для загрузки в облако
    await asyncio.sleep(4)
    return f"Uploaded to {settings.CLOUD_STORAGE_URL}/{file_path.name}"
