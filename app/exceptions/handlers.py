from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import(
    ProductNotFoundException,
    ProductOutOfStockException,
    OrderNotFoundException,
)      

def register_exception_handlers(app:FastAPI):
    """
    Register all custom exception handlers for the application
    """

    @app.exception_handler(ProductNotFoundException)
    async def product_not_found_handler(
        request:Request,
        exc:ProductNotFoundException,
    ):
        """
        Handle ProductNotFoundException.
        """
        
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'status':'error',
                'message':exc.message
            }
    )

    @app.exception_handler(ProductOutOfStockException)
    async def product_out_of_stock_handler(
        request:Request,
        exc:ProductOutOfStockException,
    ):
        """
        Handle ProductOutOfStockException.
        """
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                'status':'error',
                'message':exc.message
            }
        )
    @app.exception_handler(OrderNotFoundException)
    async def order_not_found_handler(request: Request, exc: OrderNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "error",
                "message": exc.message,
        },
    )