"""Модель объекта FileMetadata"""
from sqlalchemy.orm import Mapped, mapped_column

from src.db.session import Base


class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    extension: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)
    format: Mapped[str] = mapped_column(nullable=False)
