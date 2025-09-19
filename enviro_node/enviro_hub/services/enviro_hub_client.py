import logging
from typing import Any, Dict, Optional

from django.conf import settings

import requests

logger = logging.getLogger(__name__)


class EnviroHubClient:
    def __init__(self) -> None:
        self.base_url = settings.BASE_URL
        self.bearer_token = settings.BEARER_TOKEN
        self.verify_ssl = settings.VERIFY_SSL
        self.session = requests.Session()

        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _make_request(
        self,
        method: str,
        url: str,
        data: Optional[list[Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
    ) -> requests.Response:
        if not url.startswith(("http://", "https://")):
            url = f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"

        try:
            logger.debug(f"API Request: {method} {url}")
            logger.debug(f"Request Data: {data}")

            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=timeout,
                verify=self.verify_ssl,
            )

            logger.debug(f"API Response: {response.status_code}")
            logger.debug(f"Response Body: {response.text}")

            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"API Request failed: {method} {url} - {str(e)}")
            raise

    def post(self, url: str, data: list[Any], timeout: int = 30) -> requests.Response:
        return self._make_request("POST", url, data=data, timeout=timeout)

    def submit_data(self, url: str, data: list[Any]) -> Dict[str, Any]:
        try:
            response = self.post(url, data)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send data to {url}: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"Failed to parse JSON response from {url}: {str(e)}")
            raise
