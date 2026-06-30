from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    message: str,
    data: Any = None,
    status_code: int = 200,
) -> JSONResponse:
    response_data: dict[str, Any] = {
        "status": "success",
        "message": message,
    }

    if data is not None:
        response_data["data"] = data

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(response_data),
    )


def error_response(
    message: str,
    status_code: int = 400,
    errors: Any = None,
) -> JSONResponse:
    response_data: dict[str, Any] = {
        "status": "fail",
        "message": message,
    }

    if errors is not None:
        response_data["errors"] = errors

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(response_data),
    )
