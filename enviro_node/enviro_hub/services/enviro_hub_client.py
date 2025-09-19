import logging
from typing import Any, Dict, Optional, Union
from django.conf import settings

import requests

logger = logging.getLogger(__name__)


class EnviroHubClient:
    DEFAULT_TIMEOUT = 30
    HTTP_POST = "POST"
    CONTENT_TYPE_JSON = "application/json"

    def __init__(self) -> None:
        self.base_url = settings.BASE_URL
        self.bearer_token = settings.BEARER_TOKEN
        self.verify_ssl = settings.VERIFY_SSL
        self.session = self._create_configured_session()

    def _create_configured_session(self) -> requests.Session:
        """Create and configure a request session with authentication headers."""
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": self.CONTENT_TYPE_JSON,
            "Accept": self.CONTENT_TYPE_JSON,
        })
        return session

    def _normalize_url(self, url: str) -> str:
        """Convert relative URLs to absolute URLs using the base URL."""
        if not url.startswith(("http://", "https://")):
            return f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"
        return url

    def _make_request(
            self,
            method: str,
            url: str,
            json_data: Optional[Union[list[Any], Dict[str, Any]]] = None,
            params: Optional[Dict[str, Any]] = None,
            timeout: int = DEFAULT_TIMEOUT,
    ) -> requests.Response:
        normalized_url = self._normalize_url(url)

        try:
            logger.debug(f"API Request: {method} {normalized_url}")
            logger.debug(f"Request Data: {json_data}")

            response = self.session.request(
                method=method,
                url=normalized_url,
                json=json_data,
                params=params,
                timeout=timeout,
                verify=self.verify_ssl,
            )

            logger.debug(f"API Response: {response.status_code}")
            logger.debug(f"Response Body: {response.text}")

            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"API Request failed: {method} {normalized_url} - {str(e)}")
            raise

    def post(self, url: str, data: list[Any], timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        return self._make_request(self.HTTP_POST, url, json_data=data, timeout=timeout)

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
