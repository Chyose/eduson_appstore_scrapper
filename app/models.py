# app/models.py
from dataclasses import dataclass

@dataclass
class Review:
    author: str
    date: str
    title: str  # заголовок отзыва
    rating: int
    content: str
