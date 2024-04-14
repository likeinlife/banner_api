import structlog
from fastapi import FastAPI, Request, Response, status

logger = structlog.get_logger()


async def _logger_middleware(request: Request, call_next):
    structlog.contextvars.clear_contextvars()

    client_host = request.client.host if request.client else "unknown"

    structlog.contextvars.bind_contextvars(
        path=request.url.path,
        method=request.method,
        client_host=client_host,
    )

    response: Response = await call_next(request)

    structlog.contextvars.bind_contextvars(
        status_code=response.status_code,
    )

    if status.HTTP_400_BAD_REQUEST <= response.status_code < status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.warning("Client error")
    elif response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error("Server error")
    else:
        logger.info("OK")

    return response


def register(app: FastAPI) -> None:
    app.middleware("http")(_logger_middleware)
