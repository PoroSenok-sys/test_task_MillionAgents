import os
import sys

from fastapi import FastAPI

from src.config import settings
from src.routers.metadata import router as router_metadata
from src.routers.upload import router as router_upload

sys.path.insert(1, os.path.join(sys.path[0], '..'))

os.makedirs(settings.LOCAL_STORAGE, exist_ok=True)

app = FastAPI(
    title="Online exhibition kittens"
)

app.include_router(router_metadata)
app.include_router(router_upload)
