import pytest

from fastapi.testclient import TestClient
from sqlalchemy import select
from pathlib import Path
from aiofiles import open as aio_open

from src.db.models.metadata import FileMetadata
from src.main import app
from tests.conftest import async_session_maker

# Тестовый клиент FastAPI
client = TestClient(app)


@pytest.fixture(scope="function")
def test_file():
    file_path = Path("test_file.txt")
    with file_path.open("w") as f:
        f.write("This is a test file.")
    yield file_path
    file_path.unlink()


async def test_upload_file(test_file):
    async with aio_open(test_file, "rb") as f:
        response = client.post("/upload/", files={"file": ("test_file.txt", f, "text/plain")})

    assert response.status_code == 200
    data = response.json()
    assert "uid" in data

    # Проверяем, что файл сохранён локально
    uid = data["uid"]
    local_file_path = Path("./dir_for_uploads") / uid
    assert local_file_path.exists()

    # Проверяем сохранение метаданных в базе
    async def check_metadata():
        async with async_session_maker() as session:
            result = await session.execute(select(FileMetadata).where(FileMetadata.id == uid))
            metadata = result.scalars().first()
            assert metadata is not None
            assert metadata.filename == "test_file.txt"
            assert metadata.extension == ".txt"
            assert metadata.size > 0
            assert metadata.format == "text/plain"

    await check_metadata()

