import asyncio
import logging
from typing import Optional

import httpx

from app.config import HTTP_CONFIG

logger = logging.getLogger(__name__)


class AsyncHttpClient:
    """
    Асинхронный HTTP-клиент с retry, backoff и таймаутами.
    Вся retry-логика инкапсулирована здесь.
    """

    def __init__(self) -> None:
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "AsyncHttpClient":
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(HTTP_CONFIG.timeout),
            headers={"User-Agent": HTTP_CONFIG.user_agent},
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._client:
            await self._client.aclose()

    async def get(self, url: str) -> httpx.Response:
        assert self._client is not None, "HTTP client not initialized"

        last_exc: Optional[Exception] = None

        for attempt in range(1, HTTP_CONFIG.max_retries + 1):
            try:
                response = await self._client.get(url)

                if response.status_code < 400:
                    return response

                if response.status_code in {429, 500, 502, 503, 504}:
                    raise httpx.HTTPStatusError(
                        f"Retryable status {response.status_code}",
                        request=response.request,
                        response=response,
                    )

                response.raise_for_status()

            except (httpx.HTTPError, asyncio.TimeoutError) as exc:
                last_exc = exc
                backoff = HTTP_CONFIG.backoff_factor * (2 ** (attempt - 1))
                logger.warning(
                    "HTTP retry %s/%s for %s (sleep %.2fs): %s",
                    attempt,
                    HTTP_CONFIG.max_retries,
                    url,
                    backoff,
                    exc,
                )
                await asyncio.sleep(backoff)

        logger.error("HTTP request failed after retries: %s", url)
        raise RuntimeError("HTTP request failed") from last_exc

