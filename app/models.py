# app/models.py
from dataclasses import dataclass

@dataclass
class Review:
    """DTO для одного отзыва App Store."""
    author: str
    date: str
    title: str
    rating: int
    content: str
