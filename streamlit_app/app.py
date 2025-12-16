# streamlit_app/app.py
import sys
from pathlib import Path
import asyncio
import logging
import streamlit as st

# --- Настройка логирования ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Добавляем корень проекта в PYTHONPATH ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# --- Импортируем сервис ---
from app.service import ReviewService

# --- Streamlit UI ---
st.title("Сбор отзывов из Apple App Store")

app_id = st.text_input("Введите App ID приложения", "")

if st.button("Собрать отзывы"):
    if not app_id.strip():
        st.warning("Пожалуйста, введите корректный App ID")
    else:
        st.info("Сбор отзывов запущен...")

        async def run_scraping(app_id_input: str):
            service = ReviewService()
            try:
                reviews = await service.get_and_save_reviews(app_id_input)
                st.success(f"Собрано {len(reviews)} отзывов. Они сохранены в output/reviews.md")
            except Exception as e:
                logger.error(f"Ошибка при сборе отзывов: {e}")
                st.error(f"Ошибка: {e}")

        # Запуск асинхронной функции
        asyncio.run(run_scraping(app_id))
