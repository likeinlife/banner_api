from fastapi import FastAPI

from . import validation_error


def register_error_handlers(app: FastAPI) -> None:
    validation_error.register(app)
