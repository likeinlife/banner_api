import typing as tp

from api.dependencies.auth import Role, role_getter
from api.v1 import schemas
from api.v1.use_cases import banner_usecase_factory
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends

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
) -> schemas.BannerContentSchema:
    use_case = banner_usecase_factory(role)
    dto = await use_case.user_banner(
        role,
        banner.tag_id,
        banner.feature_id,
        banner.use_last_revision,
    )

    return schemas.BannerContentSchema(**dto.model_dump())
