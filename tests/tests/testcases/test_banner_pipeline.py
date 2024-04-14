from http import HTTPStatus

import pytest
from pydantic import TypeAdapter

from tests.enums import APIRoutes
from tests.request_sender import RequestSender

from . import schemas


@pytest.mark.run(order=0)
def test_create_banner(admin_sender: RequestSender):
    banner_content = schemas.BannerContentSchema(title="title", text="text", url="url")
    payload = schemas.CreateBannerRequest(
        tag_ids={1, 2, 3},
        feature_id=1,
        content=banner_content,
        is_active=True,
    )
    response = admin_sender.post(api_route=APIRoutes.create, body=payload.model_dump(mode="json"))
    assert response.status == HTTPStatus.OK
    TypeAdapter(schemas.CreateBannerResponse).validate_python(response.body)


@pytest.mark.run(order=1)
def test_create_banner_by_user(user_sender: RequestSender):
    banner_content = schemas.BannerContentSchema(title="title", text="text", url="url")
    payload = schemas.CreateBannerRequest(
        tag_ids={1, 2, 3},
        feature_id=1,
        content=banner_content,
        is_active=True,
    )
    response = user_sender.post(api_route=APIRoutes.create, body=payload.model_dump(mode="json"))
    assert response.status == HTTPStatus.FORBIDDEN


@pytest.mark.run(order=2)
def test_update_banner(admin_sender: RequestSender):
    banner_content = schemas.BannerContentSchema(title="UPDATED title", text="UPDATED text", url="UPDATED url")
    payload = schemas.UpdateBannerRequest(
        tag_ids={1, 2, 3},
        feature_id=1,
        content=banner_content,
        is_active=True,
    )
    url = APIRoutes.update.format(id=1)
    response = admin_sender.patch(api_route=url, body=payload.model_dump(mode="json"))
    assert response.status == HTTPStatus.OK


@pytest.mark.run(order=3)
def test_get_banner_list(admin_sender: RequestSender):
    payload = schemas.GetBannerListRequest()
    response = admin_sender.get(api_route=APIRoutes.banner_list, params=payload.model_dump(mode="json"))
    assert response.status == HTTPStatus.OK
    TypeAdapter(list[schemas.BannerSchema]).validate_python(response.body)
    assert response.body is not None
    assert len(response.body) == 1


@pytest.mark.run(order=4)
def test_user_banner(user_sender: RequestSender):
    payload = schemas.GetUserBannerRequest(
        tag_id=1,
        feature_id=1,
    )
    response = user_sender.get(api_route=APIRoutes.user_banner, params=payload.model_dump(mode="json"))
    assert response.status == HTTPStatus.OK
    TypeAdapter(schemas.BannerContentSchema).validate_python(response.body)


@pytest.mark.run(order=5)
def test_delete_banner(admin_sender: RequestSender):
    url = APIRoutes.delete.format(id=1)
    response = admin_sender.delete(api_route=url)
    assert response.status == HTTPStatus.NO_CONTENT


@pytest.mark.run(order=6)
def test_user_banner_not_found(user_sender: RequestSender):
    payload = schemas.GetUserBannerRequest(
        tag_id=1,
        feature_id=1,
        use_last_revision=True,
    )
    response = user_sender.get(api_route=APIRoutes.user_banner, params=payload.model_dump(mode="json"))
    assert response.status == HTTPStatus.NOT_FOUND
