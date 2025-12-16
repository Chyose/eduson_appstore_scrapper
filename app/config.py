# app/config.py
from typing import Dict, Set

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)

TIMEOUT: int = 10  # секунд
MAX_RETRIES: int = 5
BACKOFF_FACTOR: float = 1.5
HEADERS: Dict[str, str] = {"User-Agent": USER_AGENT}
RETRY_STATUS_CODES: Set[int] = {429, 500, 502, 503, 504}  # коды для retry
