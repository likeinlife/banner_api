import uuid

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI


def register(app: FastAPI) -> None:
    app.add_middleware(
        CorrelationIdMiddleware,
        generator=lambda: str(uuid.uuid4()),
        header_name="x-request-id",
    )
