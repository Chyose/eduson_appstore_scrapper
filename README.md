# App Store Review Scraper

## Назначение проекта
Асинхронный сервис для сбора отзывов из Apple App Store по ID приложения.  
Позволяет сохранять все отзывы в удобочитаемый Markdown-файл.

## Архитектура
Проект разделён на модули:
- `app/client.py` — HTTP-клиент с асинхронными запросами и retry.
- `app/parser.py` — парсер HTML отзывов.
- `app/models.py` — модели данных (Review и т.д.).
- `app/scraper.py` — основной сборщик отзывов.
- `app/storage.py` — сохранение отзывов в Markdown.
- `app/service.py` — бизнес-логика (связь всех компонентов).
- `streamlit_app/app.py` — пример UI через Streamlit.

## Как запустить без UI
1. Установите зависимости:
```bash
pip install -r requirements.txt

