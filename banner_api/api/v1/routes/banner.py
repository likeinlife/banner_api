import typing as tp

from api.dependencies import Role, require_admin, role_getter
from api.v1 import schemas
from api.v1.use_cases import banner_usecase_factory
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, Path, Response, status

from .utils import HttpErrorStatus as es
from .utils import get_error_responses

router = APIRouter(prefix="/banner", dependencies=[Depends(require_admin)])

role_getter_dep = tp.Annotated[Role, Depends(role_getter("Токен администратора"))]


@router.get(
    "/",
    summary="Получение всех баннеров с фильтрацией по фиче и/или тегу",  # noqa
    responses=get_error_responses([es.FORBIDDEN, es.INTERNAL, es.UNAUTHORIZED]),
)
@inject
async def banner_list(
    request: tp.Annotated[schemas.GetBannerListRequest, Depends(schemas.GetBannerListRequest)],
    paginator: tp.Annotated[schemas.Pagination, Depends(schemas.Pagination)],
    role: role_getter_dep,
) -> list[schemas.BannerSchema]:
    use_case = banner_usecase_factory(role)

    dto = await use_case.banner_list(
        tag_id=request.tag_id,
        feature_id=request.feature_id,
        offset=paginator.offset,
        limit=paginator.limit,
    )
    return [schemas.BannerSchema(**banner.model_dump()) for banner in dto]


@router.post(
    "/",
    summary="Создание нового баннера",
    responses=get_error_responses([es.FORBIDDEN, es.INTERNAL, es.UNAUTHORIZED]),
)
@inject
async def create(
    request: schemas.CreateBannerRequest,
    role: role_getter_dep,
) -> schemas.CreateBannerResponse:
    use_case = banner_usecase_factory(role)

    dto = await use_case.create(
        tag_ids=request.tag_ids,
        feature_id=request.feature_id,
        title=request.content.title,
        text=request.content.text,
        url=request.content.url,
        is_active=request.is_active,
    )
    return schemas.CreateBannerResponse(id_=dto.id_)


@router.patch(
    "/{id}/",
    summary="Обновление содержимого баннера",
    responses=get_error_responses([es.FORBIDDEN, es.INTERNAL, es.UNAUTHORIZED, es.NOT_FOUND]),
)
@inject
async def update(
    request: schemas.UpdateBannerRequest,
    id_: tp.Annotated[int, Path(alias="id")],
    role: role_getter_dep,
) -> Response:
    use_case = banner_usecase_factory(role)

    await use_case.update(
        id_=id_,
        tag_ids=request.tag_ids,
        feature_id=request.feature_id,
        title=request.content.title,
        text=request.content.text,
        url=request.content.url,
        is_active=request.is_active,
    )
    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    "/{id}/",
    summary="Удаление баннера по идентификатору",
    responses=get_error_responses([es.FORBIDDEN, es.INTERNAL, es.UNAUTHORIZED, es.NOT_FOUND]),
)
@inject
async def delete(
    id_: tp.Annotated[int, Path(alias="id")],
    role: role_getter_dep,
) -> Response:
    use_case = banner_usecase_factory(role)

    await use_case.delete(id_=id_)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
