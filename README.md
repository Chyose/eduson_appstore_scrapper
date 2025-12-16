# AppStore Review Scraper

## Назначение проекта
Асинхронный Python-сервис для сбора отзывов из Apple App Store по ID приложения.  
Позволяет сохранять отзывы в человекочитаемом Markdown формате и использовать UI на Streamlit.

## Архитектура
- **app/config.py** — конфигурация (таймауты, retry, User-Agent)
- **app/client.py** — асинхронный HTTP клиент с retry и backoff
- **app/parser.py** — парсинг HTML отзывов в Python объекты
- **app/models.py** — модели данных (Review)
- **app/scraper.py** — бизнес-логика скрапинга
- **app/storage.py** — сохранение отзывов в Markdown
- **app/service.py** — интерфейс для UI (Streamlit) или других сервисов

## Как запустить без UI
1. Установить зависимости:
```bash
pip install -r requirements.txt
