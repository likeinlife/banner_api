import typing as tp

from api.dependencies.auth import Role, role_getter
from api.v1 import schemas
from api.v1.use_cases import BannerUseCases
from container import Container
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from uow import UnitOfWork

from .utils import get_error_responses

router = APIRouter()

role_getter_dep = tp.Annotated[Role, Depends(role_getter("Токен пользователя"))]


@router.get(
    "/user_banner/",
    summary="Получение баннера пользователя",
    responses=get_error_responses(),
)
@inject
async def get(
    banner: tp.Annotated[schemas.GetUserBannerRequest, Depends(schemas.GetUserBannerRequest)],
    role: role_getter_dep,
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> schemas.BannerContentSchema:
    use_case = BannerUseCases(uow)
    dto = await use_case.user_banner(
        role,
        banner.tag_id,
        banner.feature_id,
        banner.use_last_revision,
    )

    return schemas.BannerContentSchema(**dto.model_dump())
