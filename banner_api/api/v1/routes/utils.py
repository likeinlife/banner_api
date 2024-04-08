from fastapi import status


def _prepare_error(status: int, detail: str) -> dict:
    content = {"application/json": {"example": {"error": detail}}}
    return {status: {"description": detail, "content": content}}


prepared_errors = [
    _prepare_error(status.HTTP_401_UNAUTHORIZED, "Пользователь не авторизован"),
    _prepare_error(status.HTTP_403_FORBIDDEN, "Пользователь не имеет доступа"),
    _prepare_error(status.HTTP_404_NOT_FOUND, "Баннер не найден"),
    _prepare_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "Внутренняя ошибка сервера"),
]


def get_error_responses() -> dict:
    errors = {}
    for i in prepared_errors:
        errors.update(i)
    return errors
