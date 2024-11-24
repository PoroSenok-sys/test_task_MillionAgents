"""Инструменты для работы с БД"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

async_engine = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db():
    async with async_session_factory() as session:
        yield session


class Base(DeclarativeBase):
    pass
