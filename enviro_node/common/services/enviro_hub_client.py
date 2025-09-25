from typing import Any, Dict

from django.conf import settings

from common.services import BaseHttpClient


class EnviroHubClient(BaseHttpClient):

    def __init__(self) -> None:
        super().__init__()
        self.base_url = settings.BASE_URL
        self.session.headers.update(
            {
                "Authorization": f"Bearer {settings.BEARER_TOKEN}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def submit_data(self, endpoint: str, data: list[Any]) -> Dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        response = self._make_http_request(
            "POST", url, json_data=data, verify=settings.VERIFY_SSL
        )

        return self._return_json_response(response)
