from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import(
    ProductNotFoundException,
    ProductOutOfStockException,
    OrderNotFoundException,
    InvalidTokenException,
    InvalidCredentialsException,
    PermissionDeniedException,
    InvalidPasswordException,
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

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_handler(request: Request, exc: InvalidTokenException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "error",
                "message": exc.message,
            },
        )
    
    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsException,
    ):
        """
        Handle invalid login credentials.
        """

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "error",
                "message": exc.message,
            },
        )
    @app.exception_handler(PermissionDeniedException)
    async def permission_denied_handler(
        request: Request,
        exc: PermissionDeniedException,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "status": "error",
                "message": exc.message,
            },
        )
    @app.exception_handler(InvalidPasswordException)
    async def invalid_password_handler(request,exc):
        return JSONResponse(
            status_code=400,
            content={
                "message": exc.message,
            },
        )