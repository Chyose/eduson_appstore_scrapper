from dataclasses import dataclass

@dataclass
class Review:
    author: str
    date: str
    rating: str
    text: str
