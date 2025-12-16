from pathlib import Path
from typing import List
from app.models import Review
import logging

logger = logging.getLogger(__name__)

class Storage:
    """Сохраняет отзывы в Markdown"""

    OUTPUT_FILE = Path("output/reviews.md")

    def save_reviews(self, app_name: str, reviews: List[Review]) -> None:
        if not reviews:
            logger.warning("Нет валидных отзывов для сохранения")
            return

        self.OUTPUT_FILE.parent.mkdir(exist_ok=True)

        with self.OUTPUT_FILE.open("w", encoding="utf-8") as f:
            f.write(f"# {app_name}\n")
            f.write(f"Общее количество отзывов: {len(reviews)}\n\n")

            for review in reviews:
                f.write("---\n")
                f.write(f"### {'⭐'*review.rating}{'☆'*(5-review.rating)}\n")
                f.write(f"**Автор:** {review.author}\n")
                f.write(f"**Дата:** {review.date}\n")
                f.write(f"**Заголовок:** {review.title}\n")
                f.write(f"**Текст:**\n{review.content}\n\n")

        logger.info(f"Сохранено {len(reviews)} отзывов в {self.OUTPUT_FILE}")
