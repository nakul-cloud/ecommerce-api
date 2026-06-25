from fastapi import FastAPI

from app.config.database import create_tables
from app.config.settings import APP_NAME, APP_VERSION
from app.routes.products import router as product_router
from app.exceptions.handlers import register_exception_handlers


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)

register_exception_handlers(app)

@app.on_event("startup")
def startup():
    """
    Create database tables when the application starts.
    """
    create_tables()


app.include_router(product_router)


@app.get("/")
def home():
    """
    Health check endpoint.
    """
    return {
        "message": "Welcome to the E-Commerce API"
    }