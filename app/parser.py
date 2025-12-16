# app/parser.py
from typing import List
from bs4 import BeautifulSoup
from app.models import Review
import logging

logger = logging.getLogger(__name__)

class ReviewParser:
    """Парсер HTML страницы отзывов Apple App Store."""

    def parse_reviews(self, html: str) -> List[Review]:
        """
        Преобразует HTML страницу отзывов в список объектов Review.

        Args:
            html (str): HTML-код страницы отзывов.

        Returns:
            List[Review]: Список отзывов.
        """
        soup = BeautifulSoup(html, "html.parser")
        reviews: List[Review] = []

        # Все <li> внутри секции отзывов
        review_elements = soup.select("section ul li")

        for elem in review_elements:
            try:
                # Автор
                author_tag = elem.select_one("p.author")
                author = author_tag.get_text(strip=True) if author_tag else "Unknown"

                # Дата
                date_tag = elem.select_one("time.date")
                date = date_tag["datetime"] if date_tag and date_tag.has_attr("datetime") else "Unknown"

                # Заголовок
                title_tag = elem.select_one("h3.title span.multiline-clamp__text")
                title = title_tag.get_text(strip=True) if title_tag else ""

                # Рейтинг
                rating_tag = elem.select_one("ol.stars")
                rating = len(rating_tag.select("li.star")) if rating_tag else 0

                # Текст отзыва
                content_tag = elem.select_one("p.content")
                content = content_tag.get_text(strip=True) if content_tag else ""

                reviews.append(
                    Review(
                        author=author,
                        date=date,
                        title=title,
                        rating=rating,
                        content=content
                    )
                )
            except Exception as e:
                logger.warning(f"Не удалось распарсить отзыв: {e}")

        return reviews
