from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "E-Commerce API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/ecommerce.db")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "admin123")
