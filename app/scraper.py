# app/scraper.py
from typing import List
from app.client import AsyncHTTPClient
from app.parser import ReviewParser
from app.models import Review

class AppStoreScraper:
    """Скрапинг отзывов приложения по ID"""

    BASE_URL = "https://apps.apple.com/us/app"

    def __init__(self, client: AsyncHTTPClient) -> None:
        self.client = client

    async def fetch_reviews(self, app_id: str) -> List[Review]:
        url = f"{self.BASE_URL}/id{app_id}?see-all=reviews&platform=iphone"
        html = await self.client.get(url)
        return ReviewParser.parse_reviews(html)
