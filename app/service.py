import logging
from typing import List
from app.client import AsyncHTTPClient
from app.parser import AppStoreParser
from app.storage import Storage
from app.models import Review

logger = logging.getLogger(__name__)

class ReviewService:
    """Сервис для получения и сохранения отзывов"""

    def __init__(self):
        self.client = AsyncHTTPClient()
        self.parser = AppStoreParser()
        self.storage = Storage()

    async def get_reviews(self, app_id: str, region: str = "us") -> List[Review]:
        """
        Получение отзывов по App ID.

        Args:
            app_id (str): ID приложения
            region (str): Регион App Store (по умолчанию "us")
        """
        html = await self.client.fetch_reviews(app_id, region)  # Передаем только ID
        reviews = self.parser.parse_reviews(html)
        logger.info(f"Найдено {len(reviews)} валидных отзывов для App ID {app_id}")
        return reviews

    async def get_and_save_reviews(self, app_id: str, region: str = "us") -> List[Review]:
        reviews = await self.get_reviews(app_id, region)
        if reviews:
            self.storage.save_reviews(f"App {app_id}", reviews)
        return reviews
