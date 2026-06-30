from fastapi import FastAPI, Request
import secure

secure_headers = secure.Secure.with_default_headers()


def register_security_middleware(app: FastAPI):
    """
    Register secure headers middleware for the application.
    """

    @app.middleware("http")
    async def set_secure_headers(request: Request, call_next):
        path = request.url.path
        if path in ("/docs", "/redoc", "/openapi.json"):
            return await call_next(request)
        response = await call_next(request)
        secure_headers.set_headers(response)
        return response
