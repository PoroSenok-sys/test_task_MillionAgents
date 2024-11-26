from fastapi.testclient import TestClient

from src.main import app
from tests.test_upload import test_file

# Тестовый клиент FastAPI
client = TestClient(app)


async def test_get_metadata(test_file):
    # Сначала загрузим файл
    async with test_file.open("rb") as f:
        upload_response = client.post("/upload/", files={"file": ("test_file.txt", f, "text/plain")})
    uid = upload_response.json()["uid"]

    # Получаем метаданные
    response = client.get(f"/metadata/{uid}")
    assert response.status_code == 200
    metadata = response.json()
    assert metadata["filename"] == "test_file.txt"
    assert metadata["extension"] == ".txt"


def test_metadata_not_found():
    response = client.get("/metadata/non_existing_uid")
    assert response.status_code == 404
    assert response.json()["detail"] == "File metadata not found"
