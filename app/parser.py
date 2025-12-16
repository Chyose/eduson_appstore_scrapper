from typing import List

from app.models import Review


class ReviewParser:
    """
    Отвечает ТОЛЬКО за парсинг HTML → доменные модели.
    Реализация парсинга намеренно опущена.
    """

    def parse_reviews(self, html: str) -> List[Review]:
        raise NotImplementedError(
            "HTML-парсинг отзывов должен быть реализован отдельно"
        )

