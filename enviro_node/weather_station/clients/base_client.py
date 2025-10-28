import logging
from abc import ABC
from typing import Any, Dict, Optional, Union

import requests

logger = logging.getLogger(__name__)


class BaseHttpClient(ABC):
    """Base HTTP client with common functionality for API clients."""

    DEFAULT_TIMEOUT = 30

    def __init__(self) -> None:
        self.timeout = self.DEFAULT_TIMEOUT
        self.session = requests.Session()

    def _make_http_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Union[list[Any], Dict[str, Any]]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Make an HTTP request with error handling and logging."""
        try:
            logger.info(f"HTTP Request: {method} {url}")
            logger.info(f"Request data: {json_data}")

            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=headers,
                timeout=timeout or self.timeout,
                **kwargs,
            )

            logger.info(f"HTTP Response: {response.status_code}")
            logger.info(f"Response Body: {response.text}")

            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request failed: {method} {url} - {str(e)}")
            raise

    def _return_json_response(self, response: requests.Response) -> Dict[str, Any]:
        """Return JSON response."""
        try:
            return response.json()
        except ValueError as e:
            logger.error(f"Failed to parse JSON response from: {str(e)}")
            raise
