from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import ProductNotFoundException       

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
