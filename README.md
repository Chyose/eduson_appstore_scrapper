appstore-review-scraper/
│
├── app/
│   ├── __init__.py
│   ├── config.py              # Конфигурация (URL, ретраи, таймауты)
│   ├── client.py              # HTTP-клиент с retry и async
│   ├── parser.py              # Парсинг HTML отзывов
│   ├── models.py              # DTO / dataclasses
│   ├── scraper.py             # Оркестрация процесса скрапинга
│   ├── storage.py             # Сохранение в Markdown
│   └── service.py             # Высокоуровневый сервис
│
├── streamlit_app/
│   └── app.py                 # UI (будет использовать service)
│
├── output/
│   └── reviews.md             # Результат скрапинга
│
├── requirements.txt
├── README.md
└── main.py                    # Точка входа (не UI)
