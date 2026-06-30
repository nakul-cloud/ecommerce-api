import traceback
from fastapi import status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.custom_exceptions import AppException
from app.utils.response import error_response


async def app_exception_handler(request, exc: AppException):
    """
    Handle all application-specific exceptions inheriting from AppException.
    """
    return error_response(
        message=exc.message,
        status_code=exc.status_code,
        errors=exc.errors if exc.errors else None,
    )


async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Handle validation errors (Pydantic / Request parameter validations).
    """
    errors = []
    for err in exc.errors():
        loc = err.get("loc", [])
        # Convert loc tuple/list to dot notation, removing 'body' prefix if present
        field = (
            ".".join(str(x) for x in loc[1:])
            if len(loc) > 1 and loc[0] == "body"
            else ".".join(str(x) for x in loc)
        )
        errors.append(
            {
                "field": field,
                "message": err.get("msg", "Validation error"),
            }
        )

    return error_response(
        message="Validation failed",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        errors=errors,
    )


async def http_exception_handler(request, exc: StarletteHTTPException):
    """
    Handle Starlette HTTP exceptions (like 404 Route Not Found, 405 Method Not Allowed).
    """
    return error_response(
        message=str(exc.detail),
        status_code=exc.status_code,
    )


async def global_exception_handler(request, exc: Exception):
    """
    Handle any otherwise unhandled server exceptions (HTTP 500).
    """
    # Print stack trace in development terminal
    traceback.print_exc()

    return error_response(
        message="An unexpected error occurred.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
