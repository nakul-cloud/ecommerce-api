from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Initialize limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/15 minutes"])


def register_rate_limit_middleware(app: FastAPI):
    """
    Register SlowAPI rate limiting middleware and exception handler.
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
