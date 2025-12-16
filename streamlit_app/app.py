import streamlit as st
import asyncio
from app.service import ReviewService
from pathlib import Path

st.set_page_config(page_title="App Store Reviews", layout="centered")

st.title("Сбор отзывов из App Store")

app_id = st.text_input("Введите App ID приложения", value="570060128")

if st.button("Собрать отзывы"):
    if not app_id.strip():
        st.warning("App ID не может быть пустым")
    else:
        status_text = st.empty()
        status_text.info("Сбор отзывов...")

        async def fetch_reviews(app_id: str):
            service = ReviewService()
            try:
                reviews = await service.get_and_save_reviews(app_id)
                if not reviews:
                    status_text.warning("Отзывы не найдены")
                    return None
                else:
                    status_text.success(f"Найдено {len(reviews)} отзывов")
                    # Путь к файлу
                    file_path = Path("output/reviews.md")
                    return file_path
            except Exception as e:
                status_text.error(f"Ошибка при сборе отзывов: {e}")
                return None

        # Запускаем асинхронно
        file_path = asyncio.run(fetch_reviews(app_id))

        # Предлагаем скачать файл
        if file_path and file_path.exists():
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Скачать файл с отзывами",
                    data=f,
                    file_name=file_path.name,
                    mime="text/markdown"
                )
