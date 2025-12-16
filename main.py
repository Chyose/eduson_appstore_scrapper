from app.service import AppStoreService
from app.storage import MarkdownStorage

service = AppStoreService()
storage = MarkdownStorage()

reviews, app_name = service.get_reviews("570060128")  # пример App ID
storage.save_reviews(app_name, reviews)

