from bs4 import BeautifulSoup
from typing import List
from app.models import Review

class AppStoreParser:
    """Парсер HTML страницы отзывов App Store"""

    def parse_reviews(self, html: str) -> List[Review]:
        reviews: List[Review] = []
        soup = BeautifulSoup(html, "html.parser")

        # Находим все элементы отзывов
        review_elements = soup.find_all("article", class_="svelte-1jsby4n")

        for el in review_elements:
            try:
                author_tag = el.find("p", class_="author")
                author = author_tag.get_text(strip=True) if author_tag else "Unknown"

                date_tag = el.find("time", class_="date")
                date = date_tag.get("datetime", "").strip() if date_tag else "Unknown"

                title_tag = el.find("h3", class_="title")
                title = title_tag.get_text(strip=True) if title_tag else ""

                content_tag = el.find("p", class_="content")
                content = content_tag.get_text(strip=True) if content_tag else ""

                rating_tag = el.find("ol", class_="stars")
                rating = len(rating_tag.find_all("li", class_="star")) if rating_tag else 0

                review = Review(author=author, date=date, title=title, content=content, rating=rating)

                if review.is_valid():
                    reviews.append(review)

            except Exception:
                # Игнорируем отдельные некорректные элементы
                continue

        return reviews
