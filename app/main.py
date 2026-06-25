from fastapi import FastAPI

from app.config.settings import APP_NAME, APP_VERSION
from app.config.database import create_tables

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def root():
    return {
        "message": "E-Commerce API Running"
    }