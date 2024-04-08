import typing as tp

from api.dependencies.auth import require_admin
from api.v1 import schemas
from api.v1.use_cases import BannerUseCases
from container import Container
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status
from uow import UnitOfWork

from .utils import get_error_responses

router = APIRouter(prefix="/banner", dependencies=[Depends(require_admin)])


@router.get(
    "/",
    summary="Получение всех баннеров с фильтрацией по фиче и/или тегу",
    responses=get_error_responses(),
)
@inject
async def banner_list(
    request: tp.Annotated[schemas.GetBannerListRequest, Depends(schemas.GetBannerListRequest)],
    paginator: tp.Annotated[schemas.Pagination, Depends(schemas.Pagination)],
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> list[schemas.BannerSchema]:
    use_cases = BannerUseCases(uow)

    dto = await use_cases.banner_list(
        tag_id=request.tag_id,
        feature_id=request.feature_id,
        offset=paginator.offset,
        limit=paginator.limit,
    )
    return [schemas.BannerSchema(**banner.model_dump()) for banner in dto]


@router.post(
    "/",
    summary="Создание нового баннера",
    responses=get_error_responses(),
)
@inject
async def create(
    request: schemas.CreateBannerRequest,
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> schemas.CreateBannerResponse:
    use_cases = BannerUseCases(uow)

    dto = await use_cases.create(
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
    responses=get_error_responses(),
)
@inject
async def update(
    request: schemas.UpdateBannerRequest,
    id_: tp.Annotated[int, Path(alias="id")],
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> Response:
    use_cases = BannerUseCases(uow)

    await use_cases.update(
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
    responses=get_error_responses(),
)
@inject
async def delete(
    id_: tp.Annotated[int, Path(alias="id")],
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> Response:
    use_cases = BannerUseCases(uow)

    await use_cases.delete(id_=id_)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
