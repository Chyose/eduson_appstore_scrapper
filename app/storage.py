# app/storage.py
from pathlib import Path
from typing import List
from app.models import Review
import logging

logger = logging.getLogger(__name__)

class Storage:
    """Сохранение отзывов в Markdown файл"""

    OUTPUT_FILE = Path("output/reviews.md")

    @staticmethod
    def save_reviews_md(app_name: str, reviews: List[Review]) -> None:
        Storage.OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        try:
            with Storage.OUTPUT_FILE.open("w", encoding="utf-8") as f:
                f.write(f"# Отзывы приложения: {app_name}\n")
                f.write(f"Общее количество отзывов: {len(reviews)}\n\n")

                for review in reviews:
                    stars = "⭐" * review.rating + "☆" * (5 - review.rating)
                    date_str = review.date.strftime('%Y-%m-%d') if review.date else "Неизвестно"
                    f.write("---\n")
                    f.write(f"### {stars}\n")
                    f.write(f"**Автор:** {review.author}\n")
                    f.write(f"**Дата:** {date_str}\n")
                    f.write("**Текст:**\n")
                    f.write(f"{review.content}\n\n")
            logger.info(f"Отзывы успешно сохранены в {Storage.OUTPUT_FILE}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении отзывов: {e}")
