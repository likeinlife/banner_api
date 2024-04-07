from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")


def register_v1(router: APIRouter) -> None:
    router.include_router(v1_router)
