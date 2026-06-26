from fastapi import FastAPI

from app.config.database import create_tables
from app.config.settings import APP_NAME, APP_VERSION

from app.exceptions.handlers import register_exception_handlers
from app.middleware.timing import register_middleware

from app.routes.products import router as product_router
from app.routes.orders import router as order_router
from app.routes.users import router as user_router
from app.routes.auth import router as auth_router

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)

# Register global components
register_exception_handlers(app)
register_middleware(app)


@app.on_event("startup")
def startup():
    """
    Create database tables when the application starts.
    """
    create_tables()


# Register application routers
app.include_router(product_router)
app.include_router(order_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
def home():
    """
    Health check endpoint.
    """
    return {
        "message": "Welcome to the E-Commerce API"
    }