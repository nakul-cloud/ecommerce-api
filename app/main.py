from contextlib import asynccontextmanager
import sys
from starlette.exceptions import HTTPException as StarletteHTTPException

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config.database import create_tables, get_db_connection
from app.routes.index import app_routes
from app.config.settings import settings
from fastapi.exceptions import RequestValidationError
from app.exceptions.handlers import (
    app_exception_handler,
    validation_exception_handler,
    global_exception_handler,
    http_exception_handler,
)
from app.exceptions.custom_exceptions import AppException
from app.utils.logger import logger

# Import middlewares
from app.middleware.timing import register_middleware as register_timing_middleware
from app.middleware.security import register_security_middleware
from app.middleware.rate_limit import register_rate_limit_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Authenticating underlying relational database configurations...")
        create_tables()
        conn = get_db_connection()
        conn.execute("SELECT 1")
        conn.close()
        logger.info("Database connectivity verified successfully.")
    except Exception as e:
        logger.critical(f"Database connection handshake failed: {e}")
        raise e

    logger.info(f"Application initialized: {settings.app_name}")
    logger.info(f"Environment Profile: {settings.env}")
    logger.info(f"Binding network listeners onto port: {settings.port}")

    yield  # app runs here

    logger.info("Commencing shutdown logic...")
    logger.info("Shutdown procedure complete.")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs" if settings.env == "development" else None,
    lifespan=lifespan,
)

# Register application routers
api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(app_routes)
app.include_router(api_v1_router)

# Register Custom Middlewares
register_timing_middleware(app)
register_security_middleware(app)
register_rate_limit_middleware(app)

# GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS
allowed_origins = settings.allowed_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)


# --- CUSTOM EXCEPTION HANDLERS ---
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)


@app.get("/")
def home():
    """
    Health check endpoint.
    """
    from app.utils.response import success_response
    return success_response(message="Welcome to the E-Commerce API")


def start_server():
    """Start the FastAPI server directly via Uvicorn execution entry point."""
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=settings.port,
            reload=(settings.env == "development"),
            reload_dirs=["app"] if settings.env == "development" else None,
            log_level="info",
        )
    except Exception as error:
        logger.critical(
            f"CRITICAL SYSTEM EXECUTION ENGINES COMPROMISED! Failed to start server: {error}"
        )
        sys.exit(1)


if __name__ == "__main__":
    start_server()
