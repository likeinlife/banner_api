from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse


async def request_validation_exception_handler(_: Request, exc: RequestValidationError) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": jsonable_encoder(exc.errors(), exclude={"url"}),
        },
    )


def register(app: FastAPI) -> None:
    app.exception_handler(RequestValidationError)(request_validation_exception_handler)
