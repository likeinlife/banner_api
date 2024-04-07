from fastapi import APIRouter, Depends, Path, Query

from . import schemas

router = APIRouter(prefix="/banner")


@router.get("/", summary="Получение всех баннеров с фильтрацией по фиче и/или тегу")
def list(
    request: schemas.GetBannerListRequest = Depends(schemas.GetBannerListRequest),
    token: str = Query(description="Токен пользователя"),
):
    raise NotImplementedError


@router.post("/", summary="Создание нового баннера")
def create(
    request: schemas.CreateBannerRequest,
    token: str = Query(description="Токен админа"),
):
    raise NotImplementedError


@router.patch("/{id}/", summary="Обновление содержимого баннера")
def update(
    request: schemas.UpdateBannerRequest,
    id_: int = Path(alias="id"),
    token: str = Query(description="Токен админа"),
):
    raise NotImplementedError


@router.delete("/{id}/", summary="Удаление баннера по идентификатору")
def delete(
    id_: int = Path(alias="id"),
    token: str = Query(description="Токен админа"),
):
    raise NotImplementedError
