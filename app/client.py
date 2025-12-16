# app/client.py
import asyncio
import logging
from typing import Optional

import httpx
from app.config import TIMEOUT, MAX_RETRIES, BACKOFF_FACTOR, HEADERS

logger = logging.getLogger(__name__)

class AsyncHTTPClient:
    """Асинхронный HTTP клиент с retry, таймаутами и exponential backoff"""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS)

    async def get(self, url: str, params: Optional[dict] = None) -> str:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await self.client.get(url, params=params)
                if response.status_code in {429, 500, 502, 503, 504}:
                    raise httpx.HTTPStatusError(
                        f"Server error: {response.status_code}", request=response.request, response=response
                    )
                return response.text
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                wait_time = BACKOFF_FACTOR ** attempt
                logger.warning(f"Попытка {attempt}/{MAX_RETRIES} не удалась: {e}. Ждем {wait_time:.1f} сек")
                await asyncio.sleep(wait_time)
        logger.error(f"Не удалось получить данные с {url} после {MAX_RETRIES} попыток")
        raise RuntimeError(f"Не удалось получить данные с {url}")
    
    async def close(self):
        await self.client.aclose()
