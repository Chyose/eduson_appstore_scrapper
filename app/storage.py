from pathlib import Path
from typing import Iterable

from app.models import Review


class ReviewStorage:
    """
    Отвечает только за сохранение данных.
    """

    def save_markdown(self, reviews: Iterable[Review], path: Path) -> None:
        lines: list[str] = ["# App Store Reviews\n"]

        for review in reviews:
            lines.extend(
                [
                    f"## {review.title}",
                    f"- Автор: {review.author}",
                    f"- Рейтинг: {review.rating}",
                    f"- Дата: {review.review_date}",
                    "",
                    review.body,
                    "",
                ]
            )

        path.write_text("\n".join(lines), encoding="utf-8")

