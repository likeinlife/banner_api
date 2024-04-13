from enum import Enum

from fastapi import status


class HttpErrorStatus(Enum):
    UNAUTHORIZED = (status.HTTP_401_UNAUTHORIZED, "Пользователь не авторизован")
    FORBIDDEN = (status.HTTP_403_FORBIDDEN, "Пользователь не имеет доступа")
    NOT_FOUND = (status.HTTP_404_NOT_FOUND, "Баннер не найден")
    INTERNAL = (status.HTTP_500_INTERNAL_SERVER_ERROR, "Внутренняя ошибка сервера")


def _prepare_error(status: int, detail: str) -> dict:
    content = {"application/json": {"example": {"error": detail}}}
    return {status: {"description": detail, "content": content}}


def get_error_responses(error_list: list[HttpErrorStatus]) -> dict:
    errors = {}
    for error in error_list:
        prepared = _prepare_error(error.value[0], error.value[1])
        errors.update(prepared)
    return errors
