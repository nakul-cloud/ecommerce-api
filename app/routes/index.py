from fastapi import APIRouter

from app.routes.auth_routes import router as auth_router
from app.routes.order_routes import router as order_router
from app.routes.product_routes import router as product_router
from app.routes.user_routes import router as user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(product_router)
router.include_router(order_router)

app_routes = router

