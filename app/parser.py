# app/parser.py
from typing import List
from datetime import datetime
from bs4 import BeautifulSoup
from app.models import Review
import logging

logger = logging.getLogger(__name__)

class ReviewParser:
    """Парсер HTML страницы отзывов Apple App Store"""

    @staticmethod
    def parse_reviews(html: str) -> List[Review]:
        soup = BeautifulSoup(html, "html.parser")
        reviews: List[Review] = []

        review_divs = soup.find_all("div", class_="we-customer-review")
        if not review_divs:
            logger.warning("Не найдено отзывов на странице")
            return reviews

        for div in review_divs:
            try:
                author_tag = div.find("span", class_="we-truncate we-truncate--single-line")
                author = author_tag.get_text(strip=True) if author_tag else "Неизвестно"

                date_tag = div.find("time")
                date_str = date_tag["datetime"] if date_tag and date_tag.has_attr("datetime") else None
                date = datetime.fromisoformat(date_str) if date_str else None

                rating_tag = div.find("figure", class_="we-star-rating")
                rating = 0
                if rating_tag:
                    aria_label = rating_tag.get("aria-label")
                    if aria_label:
                        try:
                            rating = int(aria_label.split()[0])
                        except ValueError:
                            rating = 0

                title_tag = div.find("h3", class_="we-truncate")
                title = title_tag.get_text(strip=True) if title_tag else ""

                content_tag = div.find("blockquote")
                content = content_tag.get_text(strip=True) if content_tag else ""

                reviews.append(
                    Review(
                        author=author,
                        title=title,
                        content=content,
                        rating=rating,
                        date=date,
                        version=None
                    )
                )
            except Exception as e:
                logger.error(f"Ошибка парсинга одного отзыва: {e}")
                continue

        return reviews
