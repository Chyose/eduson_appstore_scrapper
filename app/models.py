# app/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Review:
    author: str
    title: str
    content: str
    rating: int
    date: datetime
    version: Optional[str] = None
