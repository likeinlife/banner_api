from contextlib import asynccontextmanager

from api import register_api_routes
from container import Container
from core import settings
from fastapi import FastAPI, Response, status
from fastapi.responses import ORJSONResponse
from middlewares import register_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    container.init_resources()
    yield
    container.shutdown_resources()


app = FastAPI(
    title=settings.app.title,
    version=settings.app.version,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

register_api_routes(app)
register_middlewares(app)


@app.get(
    "/health/",
    tags=["healthcheck"],
    status_code=status.HTTP_200_OK,
)
def healthcheck() -> Response:
    return Response(status_code=status.HTTP_200_OK)
