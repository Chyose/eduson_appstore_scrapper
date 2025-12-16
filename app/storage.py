import logging
from pathlib import Path
from typing import List
from .models import Review

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class MarkdownStorage:
    """
    Класс для сохранения отзывов в Markdown-файл.
    """

    def __init__(self, output_path: str = "output/reviews.md") -> None:
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"MarkdownStorage инициализирован с файлом {self.output_path}")

    def save_reviews(self, app_name: str, reviews: List[Review]) -> None:
        """
        Сохраняет список отзывов в Markdown-файл.
        
        :param app_name: Название приложения
        :param reviews: Список объектов Review
        """
        logger.info(f"Сохраняем {len(reviews)} отзывов для приложения '{app_name}' в Markdown")
        try:
            with self.output_path.open("w", encoding="utf-8") as f:
                f.write(f"# {app_name}\n\n")
                f.write(f"Общее количество отзывов: {len(reviews)}\n\n")

                for review in reviews:
                    f.write("---\n")
                    f.write(f"### {review.rating}⭐\n")
                    f.write(f"**Автор:** {review.author}\n\n")
                    f.write(f"**Дата:** {review.date}\n\n")
                    f.write(f"**Текст:**\n{review.text}\n\n")
            logger.info(f"Отзывы успешно сохранены в {self.output_path}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении Markdown: {e}")
