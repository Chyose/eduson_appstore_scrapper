# app/config.py
from typing import Dict

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

TIMEOUT = 10  # сек
MAX_RETRIES = 5
BACKOFF_FACTOR = 1.5  # экспоненциальный backoff
HEADERS: Dict[str, str] = {"User-Agent": USER_AGENT}
