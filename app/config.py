from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class HttpConfig:
    timeout: float = 10.0
    max_retries: int = 5
    backoff_factor: float = 0.5
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )


@dataclass(frozen=True)
class AppStoreConfig:
    base_url: Final[str] = "https://apps.apple.com"
    country: str = "us"
    platform: str = "iphone"


HTTP_CONFIG = HttpConfig()
APPSTORE_CONFIG = AppStoreConfig()

