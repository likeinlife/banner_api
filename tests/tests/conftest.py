import pytest

from tests.request_sender import RequestSender
from tests.settings import settings


@pytest.fixture(scope="session")
def admin_sender() -> RequestSender:
    return RequestSender(is_admin=True, domain=settings.domain, api_url=settings.api_url)


@pytest.fixture(scope="session")
def user_sender() -> RequestSender:
    return RequestSender(is_admin=False, domain=settings.domain, api_url=settings.api_url)
