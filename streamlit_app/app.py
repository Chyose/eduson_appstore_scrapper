# streamlit_app/app.py
import streamlit as st
import asyncio
import logging
import sys
from pathlib import Path

from app.service import ReviewService

# Добавляем корень проекта в PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.service import ReviewService


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Заголовок UI
st.title("Сбор отзывов из Apple App Store")

# Поле ввода App ID
app_id = st.text_input("Введите App ID приложения", "")

# Кнопка запуска
if st.button("Собрать отзывы"):
    if not app_id.strip():
        st.warning("Пожалуйста, введите корректный App ID")
    else:
        st.info("Сбор отзывов запущен...")

        async def run_scraping():
            service = ReviewService()
            try:
                reviews = await service.get_and_save_reviews(app_id)
                st.success(f"Собрано {len(reviews)} отзывов. Они сохранены в output/reviews.md")
            except Exception as e:
                logger.error(f"Ошибка при сборе отзывов: {e}")
                st.error(f"Ошибка: {e}")

        asyncio.run(run_scraping())
