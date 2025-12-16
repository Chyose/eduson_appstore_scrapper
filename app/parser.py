from __future__ import annotations

from typing import List, Optional
from datetime import datetime

from bs4 import BeautifulSoup

from app.models import Review


class AppStoreReviewParser:
    """
    Парсер HTML-страницы отзывов Apple App Store.

    Ответственность:
    - принимает HTML
    - извлекает отзывы
    - возвращает список доменных объектов Review

    ВАЖНО:
    - не делает HTTP-запросы
    - не пишет файлы
    """

    def parse(self, html: str) -> List[Review]:
        """
        Основная точка входа.

        :param html: HTML страницы отзывов App Store
        :return: список Review
        """
        soup = BeautifulSoup(html, "html.parser")
        review_blocks = soup.select("div.we-customer-review")

        reviews: List[Review] = []

        for block in review_blocks:
            review = self._parse_single_review(block)
            if review:
                reviews.append(review)

        return reviews

    def _parse_single_review(self, block) -> Optional[Review]:
        """
        Парсинг одного отзыва.
        При ошибках или отсутствии ключевых данных — возвращает None.
        """
        try:
            username = self._parse_username(block)
            rating = self._parse_rating(block)
            text = self._parse_text(block)
            date = self._parse_date(block)

            # Минимальная валидация
            if not text:
                return None

            return Review(
                username=username or "Unknown",
                rating=rating,
                text=text,
                date=date,
            )
        except Exception:
            # Защита от неожиданных изменений HTML
            return None

    @staticmethod
    def _parse_username(block) -> Optional[str]:
        """
        Имя пользователя.
        """
        el = block.select_one(".we-customer-review__user")
        return el.get_text(strip=True) if el else None

    @staticmethod
    def _parse_rating(block) -> Optional[int]:
        """
        Рейтинг в звёздах.

        Apple хранит рейтинг в атрибуте:
        aria-label="5 out of 5"
        """
        el = block.select_one(".we-star-rating")
        if not el:
            return None

        aria_label = el.get("aria-label", "")
        try:
            return int(aria_label.split()[0])
        except (ValueError, IndexError):
            return None

    @staticmethod
    def _parse_text(block) -> Optional[str]:
        """
        Текст отзыва.

        Иногда Apple разбивает текст на несколько <p>.
        """
        paragraphs = block.select(
            ".we-customer-review__body p"
        )
        if not paragraphs:
            return None

        return "\n".join(p.get_text(strip=True) for p in paragraphs)

    @staticmethod
    def _parse_date(block) -> Optional[datetime]:
        """
        Дата отзыва.
        """
        el = block.select_one("time")
        if not el:
            return None

        date_str = el.get("datetime")
        if not date_str:
            return None

        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            return None
