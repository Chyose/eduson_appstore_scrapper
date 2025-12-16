# app/parser.py
from bs4 import BeautifulSoup
from typing import List
from app.models import Review

class ReviewParser:
    """Парсер HTML страниц с отзывами"""

    @staticmethod
    def parse_reviews(html: str) -> List[Review]:
        # Здесь будет логика BeautifulSoup
        # Пока заглушка
        return []
