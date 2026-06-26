from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "E-Commerce API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/ecommerce.db")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)
ADMIN_REGISTRATION_KEY = os.getenv("ADMIN_REGISTRATION_KEY")