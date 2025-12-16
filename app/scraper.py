import logging
from typing import List

from app.client import AsyncHttpClient
from app.config import APPSTORE_CONFIG
from app.models import Review
from app.parser import ReviewParser

logger = logging.getLogger(__name__)


class AppStoreScraper:
    """
    Оркестратор процесса скрапинга.
    Не знает ничего о хранении и UI.
    """

    def __init__(
        self,
        http_client: AsyncHttpClient,
        parser: ReviewParser,
    ) -> None:
        self._http_client = http_client
        self._parser = parser

    def _build_reviews_url(self, app_id: str) -> str:
        return (
            f"{APPSTORE_CONFIG.base_url}/"
            f"{APPSTORE_CONFIG.country}/app/id{app_id}"
            f"?see-all=reviews&platform={APPSTORE_CONFIG.platform}"
        )

    async def fetch_reviews(self, app_id: str) -> List[Review]:
        url = self._build_reviews_url(app_id)
        logger.info("Fetching reviews from %s", url)

        response = await self._http_client.get(url)
        return self._parser.parse_reviews(response.text)

