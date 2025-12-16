# app/service.py
from typing import List
from app.client import AsyncHTTPClient
from app.scraper import AppStoreScraper
from app.storage import Storage
from app.models import Review
import asyncio
import logging

logger = logging.getLogger(__name__)

class ReviewService:
    """Сервис для UI или других сервисов"""

    def __init__(self) -> None:
        self.client = AsyncHTTPClient()
        self.scraper = AppStoreScraper(self.client)

    async def get_and_save_reviews(self, app_id: str, app_name: str = "") -> List[Review]:
        reviews: List[Review] = []
        try:
            reviews = await self.scraper.fetch_reviews(app_id)
            Storage.save_reviews_md(app_name or app_id, reviews)
        except Exception as e:
            logger.error(f"Ошибка при сборе/сохранении отзывов: {e}")
            raise
        finally:
            await self.client.close()
        return reviews
