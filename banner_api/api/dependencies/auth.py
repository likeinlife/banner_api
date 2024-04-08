import enum
import typing as tp

from fastapi import Depends, Header, HTTPException, status


class Role(enum.Enum):
    ADMIN = "admin"
    USER = "user"


def role_getter(header_description: str):
    async def get_current_role(
        token: tp.Annotated[str | None, Header(description=header_description)] = None,
    ) -> Role:
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован")
        if token.startswith("-"):
            return Role.ADMIN
        return Role.USER

    return get_current_role


def require_admin(role: tp.Annotated[Role, Depends(role_getter("Токен администратора"))]):
    if role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь не имеет доступа")
