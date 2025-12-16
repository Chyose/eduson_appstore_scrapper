import logging
from pathlib import Path

from app.client import AsyncHttpClient
from app.parser import ReviewParser
from app.scraper import AppStoreScraper
from app.storage import ReviewStorage

logger = logging.getLogger(__name__)


class ReviewScrapingService:
    """
    Фасад уровня приложения.
    Удобен для CLI, Streamlit, API.
    """

    def __init__(self) -> None:
        self._parser = ReviewParser()
        self._storage = ReviewStorage()

    async def run(self, app_id: str, output_path: Path) -> None:
        async with AsyncHttpClient() as http_client:
            scraper = AppStoreScraper(http_client, self._parser)
            reviews = await scraper.fetch_reviews(app_id)

        self._storage.save_markdown(reviews, output_path)
        logger.info("Saved %s reviews to %s", len(reviews), output_path)

