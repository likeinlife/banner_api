import typing as tp

from api.dependencies.auth import Role, role_getter
from fastapi import APIRouter, Depends, Path

from . import schemas

router = APIRouter(prefix="/banner")

get_role_dep = tp.Annotated[Role, Depends(role_getter("Токен администратора"))]


@router.get("/", summary="Получение всех баннеров с фильтрацией по фиче и/или тегу")
def list(
    request: tp.Annotated[schemas.GetBannerListRequest, Depends(schemas.GetBannerListRequest)],
    paginator: tp.Annotated[schemas.Pagination, Depends(schemas.Pagination)],
    role: get_role_dep,
):
    raise NotImplementedError


@router.post("/", summary="Создание нового баннера")
def create(
    request: schemas.CreateBannerRequest,
    role: get_role_dep,
):
    raise NotImplementedError


@router.patch("/{id}/", summary="Обновление содержимого баннера")
def update(
    request: schemas.UpdateBannerRequest,
    id_: tp.Annotated[int, Path(alias="id")],
    role: get_role_dep,
):
    raise NotImplementedError


@router.delete("/{id}/", summary="Удаление баннера по идентификатору")
def delete(
    id_: tp.Annotated[int, Path(alias="id")],
    role: get_role_dep,
):
    raise NotImplementedError
