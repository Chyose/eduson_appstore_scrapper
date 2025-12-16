# app/storage.py
from typing import List
from app.models import Review
from pathlib import Path
import datetime

class Storage:
    """Сохранение и загрузка отзывов"""

    OUTPUT_FILE = Path("output/reviews.md")

    @staticmethod
    def save_reviews(reviews: List[Review]):
        Storage.OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with Storage.OUTPUT_FILE.open("w", encoding="utf-8") as f:
            for review in reviews:
                f.write(f"### {review.title} ({review.rating}⭐)\n")
                f.write(f"Автор: {review.author}\n")
                f.write(f"Дата: {review.date.strftime('%Y-%m-%d')}\n")
                f.write(f"Версия: {review.version or '—'}\n")
                f.write(f"{review.content}\n\n")
