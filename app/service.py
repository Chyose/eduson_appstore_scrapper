# app/service.py
from app.client import AsyncHTTPClient
from app.parser import ReviewParser
from app.storage import Storage
import logging

logger = logging.getLogger(__name__)

class ReviewService:
    """Сервис для получения и сохранения отзывов App Store."""

    async def get_and_save_reviews(self, app_id: str):
        """Получает HTML, парсит отзывы и сохраняет их в Markdown."""
        client = AsyncHTTPClient()
        try:
            html = await client.fetch_reviews(app_id)
        except Exception as e:
            logger.error(f"Ошибка при получении HTML: {e}")
            raise

        parser = ReviewParser()
        reviews = parser.parse_reviews(html)

        if not reviews:
            logger.warning(f"Отзывы для приложения {app_id} не найдены.")

        Storage().save_reviews(app_id, reviews)
        return reviews
