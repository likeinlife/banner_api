from fastapi import APIRouter, Depends, Query

from . import schemas

router = APIRouter()


@router.get("/user_banner/", summary="Получение баннера пользователя")
def get(
    banner: schemas.GetUserBannerRequest = Depends(schemas.GetUserBannerRequest),
    token: str = Query(),
) -> schemas.BannerContentSchema:
    raise NotImplementedError
