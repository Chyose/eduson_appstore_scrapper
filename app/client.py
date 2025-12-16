# app/client.py
import httpx
import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AsyncHTTPClient:
    """Асинхронный HTTP клиент с retry и таймаутами для App Store."""

    BASE_URL = "https://apps.apple.com"

    def __init__(self, timeout: float = 10.0, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    async def fetch_reviews(self, app_id: str, region: str = "us") -> str:
    """
    Получает HTML страницу всех отзывов приложения по App ID.

    Args:
        app_id (str): ID приложения.
        region (str): Регион App Store (по умолчанию "us").

    Returns:
        str: HTML код страницы.
    """
    url = f"{self.BASE_URL}/{region}/app/id{app_id}?see-all=reviews&platform=iphone"

    for attempt in range(1, self.max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers, follow_redirects=True) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.text
                elif response.status_code in {429, 500, 502, 503, 504}:
                    logger.warning(f"Попытка {attempt}: сервер вернул {response.status_code}, retrying...")
                    await asyncio.sleep(2 ** attempt)
                else:
                    response.raise_for_status()
        except httpx.RequestError as e:
            logger.warning(f"Попытка {attempt}: ошибка запроса {e}, retrying...")
            await asyncio.sleep(2 ** attempt)

    raise RuntimeError(f"Не удалось получить HTML после {self.max_retries} попыток")

