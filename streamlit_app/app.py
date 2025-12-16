import streamlit as st
import logging
from app.service import AppStoreService

# Настройка логирования Streamlit
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title="App Store Reviews Scraper", layout="centered")
st.title("Сбор отзывов из App Store")

app_id = st.text_input("Введите App ID приложения:")

if st.button("Собрать отзывы"):
    if not app_id.strip():
        st.warning("Пожалуйста, введите корректный App ID.")
    else:
        st.info("Сбор отзывов запущен...")
        service = AppStoreService()
        try:
            reviews, app_name = service.get_reviews(app_id)
            st.success(f"Собрано {len(reviews)} отзывов для приложения '{app_name}'")
        except Exception as e:
            logger.exception("Ошибка при сборе отзывов")
            st.error(f"Произошла ошибка: {e}")

