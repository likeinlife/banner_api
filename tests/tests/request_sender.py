import random
import typing as tp
from dataclasses import dataclass

import requests
from requests.adapters import CaseInsensitiveDict


@dataclass
class Response:
    status: int
    body: dict | list | None
    headers: CaseInsensitiveDict


class RequestSender:
    """
    Request sender for test purposes.

    Example api_route for methods: /user_banner/

    Args
    ----
        is_admin: Is admin or not
        domain: Domain. Example: http://127.0.0.1:8000
        api_url: API url. Eample: /api/v1
    """

    def __init__(self, is_admin: bool, domain: str, api_url: str) -> None:
        self._api = domain + api_url

        _id = random.randint(-1000, -1)
        self._id = _id if is_admin else _id * -1
        self._timeout = 5

    def post(self, api_route: str, body: dict[str, tp.Any], params: dict[str, tp.Any] | None = None) -> Response:
        response = requests.post(
            self._api + api_route,
            json=body,
            params=params,
            timeout=self._timeout,
            headers=self._headers,
        )

        response_body = response.json() if response.content else None
        return Response(status=response.status_code, body=response_body, headers=response.headers)

    def get(self, api_route: str, params: dict[str, tp.Any]) -> Response:
        response = requests.get(
            self._api + api_route,
            params=params,
            timeout=self._timeout,
            headers=self._headers,
        )

        response_body = response.json() if response.content else None
        return Response(status=response.status_code, body=response_body, headers=response.headers)

    def delete(self, api_route: str, params: dict[str, tp.Any] | None = None) -> Response:
        response = requests.delete(
            self._api + api_route,
            params=params,
            timeout=self._timeout,
            headers=self._headers,
        )

        response_body = response.json() if response.content else None
        return Response(status=response.status_code, body=response_body, headers=response.headers)

    def patch(self, api_route: str, body: dict[str, tp.Any], params: dict[str, tp.Any] | None = None) -> Response:
        response = requests.patch(
            self._api + api_route,
            params=params,
            json=body,
            timeout=self._timeout,
            headers=self._headers,
        )

        response_body = response.json() if response.content else None
        return Response(status=response.status_code, body=response_body, headers=response.headers)

    @property
    def _headers(self) -> dict[str, str]:
        return {"token": str(self._id)}
