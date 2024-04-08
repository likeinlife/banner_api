from fastapi import APIRouter

from .routes import banner, user_banner

v1_router = APIRouter(prefix="/v1", tags=["v1"])


def register_v1(router: APIRouter) -> None:
    v1_router.include_router(user_banner.router)
    v1_router.include_router(banner.router)
    router.include_router(v1_router)
