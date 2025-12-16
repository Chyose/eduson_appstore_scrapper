from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class Review:
    author: str
    rating: int
    title: str
    body: str
    review_date: date

