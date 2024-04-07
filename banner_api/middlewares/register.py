from fastapi import FastAPI

from . import correlation, logger


def register_middlewares(app: FastAPI) -> None:
    logger.register(app)
    correlation.register(app)
