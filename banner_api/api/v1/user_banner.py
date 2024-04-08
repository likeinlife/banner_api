import typing as tp

from api.dependencies.auth import Role, role_getter
from fastapi import APIRouter, Depends

from . import schemas

router = APIRouter()

role_getter_dep = tp.Annotated[Role, Depends(role_getter("Токен пользователя"))]


@router.get("/user_banner/", summary="Получение баннера пользователя")
async def get(
    banner: tp.Annotated[schemas.GetUserBannerRequest, Depends(schemas.GetUserBannerRequest)],
    role: role_getter_dep,
) -> schemas.BannerContentSchema:
    raise NotImplementedError
