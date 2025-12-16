# app/service.py
from typing import List
from app.client import AsyncHTTPClient
from app.scraper import AppStoreScraper
from app.storage import Storage
from app.models import Review
import asyncio

class ReviewService:
    """Сервис для UI или других сервисов"""

    def __init__(self):
        self.client = AsyncHTTPClient()
        self.scraper = AppStoreScraper(self.client)

    async def get_and_save_reviews(self, app_id: str) -> List[Review]:
        reviews = await self.scraper.fetch_reviews(app_id)
        Storage.save_reviews(reviews)
        await self.client.close()
        return reviews
