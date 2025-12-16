# app/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Review:
    """Модель данных для отзыва"""
    author: str
    title: str
    content: str
    rating: int
    date: Optional[datetime]
    version: Optional[str] = None
