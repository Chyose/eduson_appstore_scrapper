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

        review_elements = soup.find_all("li", {"class": "svelte-1jsby4n"})

        for elem in review_elements:
            try:
                # Автор
                author_tag = elem.find("p", class_="author")
                author = author_tag.get_text(strip=True) if author_tag else "Unknown"

                # Дата
                date_tag = elem.find("time", class_="date")
                date = date_tag["datetime"] if date_tag and date_tag.has_attr("datetime") else "Unknown"

                # Заголовок
                title_tag = elem.find("h3", class_="title")
                title_span = title_tag.find("span", class_="multiline-clamp__text") if title_tag else None
                title = title_span.get_text(strip=True) if title_span else ""

                # Рейтинг
                rating_tag = elem.find("ol", class_="stars")
                rating = 0
                if rating_tag:
                    stars = rating_tag.find_all("li", class_="star")
                    rating = len(stars)

                # Текст отзыва
                content_tag = elem.find("p", class_="content")
                content = content_tag.get_text(strip=True) if content_tag else ""

                review = Review(
                    author=author,
                    date=date,
                    title=title,
                    rating=rating,
                    content=content
                )
                reviews.append(review)
            except Exception as e:
                logger.warning(f"Не удалось распарсить отзыв: {e}")

        return reviews
