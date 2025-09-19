import logging
from typing import Dict, Optional, Union

from django.conf import settings

import requests


class OpenWeatherClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    ICON_BASE_URL = "https://openweathermap.org/img/wn"
    DEFAULT_TIMEOUT = 30
    DEFAULT_UNITS = "metric"
    DEFAULT_LANG = "de"
    DEFAULT_ICON_SIZE = "2x"

    def __init__(self) -> None:
        self.api_key = settings.API_KEY
        self.city_name = settings.CITY_NAME
        self.base_url = self.BASE_URL
        self.timeout = self.DEFAULT_TIMEOUT
        self._validate_configuration()

    def _validate_configuration(self) -> None:
        if not self.api_key:
            raise ValueError("API_KEY must be set in settings.py")

    def _make_request(self, endpoint: str, params: Dict[str, Union[str, int]]) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        params["appid"] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"API request failed for {endpoint}: {e}")
            raise

    def get_current_weather(
        self, city: Optional[str] = None, units: str = DEFAULT_UNITS, lang: str = DEFAULT_LANG
    ) -> Dict:
        city = city or self.city_name
        if not city:
            raise ValueError("CITY_NAME must be set in settings.py")

        params = {"q": city, "units": units, "lang": lang}

        return self._make_request("weather", params)

    def get_icon_url(self, icon_code: str, size: str = DEFAULT_ICON_SIZE) -> str:
        return f"{self.ICON_BASE_URL}/{icon_code}@{size}.png"
