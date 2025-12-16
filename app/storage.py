# app/storage.py
from typing import List
from app.models import Review
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Storage:
    """Сохраняет отзывы в Markdown файл."""

    def __init__(self, output_path: str = "output/reviews.md"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def save_reviews(self, app_id: str, reviews: List[Review]):
        """Сохраняет список отзывов в Markdown файл."""
        if not reviews:
            logger.warning(f"Нет отзывов для сохранения по приложению {app_id}")
            return

        app_title = reviews[0].title or f"App {app_id}"
        md_lines = [
            f"# Отзывы для {app_title}\n",
            f"Общее количество отзывов: {len(reviews)}\n"
        ]

        for review in reviews:
            stars = "⭐" * review.rating + "☆" * (5 - review.rating)
            md_lines.extend([
                "---",
                f"### {stars}",
                f"**Автор:** {review.author}",
                f"**Дата:** {review.date}",
                f"**Заголовок:** {review.title}",
                f"**Текст:**\n{review.content}\n"
            ])

        try:
            self.output_path.write_text("\n".join(md_lines), encoding="utf-8")
            logger.info(f"Отзывы сохранены в {self.output_path}")
        except Exception as e:
            logger.error(f"Не удалось сохранить отзывы: {e}")
