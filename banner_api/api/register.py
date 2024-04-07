from fastapi import APIRouter, FastAPI

from .v1 import register_v1

router = APIRouter(prefix="/api")


def register_api_routes(app: FastAPI) -> None:
    register_v1(router)

    app.include_router(router)
