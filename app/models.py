from dataclasses import dataclass
from typing import Optional

@dataclass
class Review:
    author: str
    date: str
    title: str
    content: str
    rating: int

    def is_valid(self) -> bool:
        """Проверка, что отзыв содержит хотя бы один значимый элемент"""
        if self.author in ("", "Unknown") and self.date in ("", "Unknown") and not self.content.strip():
            return False
        return True
