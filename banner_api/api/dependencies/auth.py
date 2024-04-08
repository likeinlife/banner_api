import enum

from fastapi import Header, Request


class Role(enum.Enum):
    ADMIN = "admin"
    USER = "user"


def role_getter(header_description: str):
    async def get_current_role(request: Request, token: str = Header(description=header_description)) -> Role:
        if token.startswith("-"):
            return Role.ADMIN
        return Role.USER

    return get_current_role
