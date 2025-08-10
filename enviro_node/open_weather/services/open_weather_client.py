import logging
from typing import Dict, Optional, Union

from django.conf import settings

import requests


class OpenWeatherClient:

    def __init__(self) -> None:
        self.api_key = settings.API_KEY
        self.city_name = settings.CITY_NAME
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.timeout = 30

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
        self, city: Optional[str] = None, units: str = "metric", lang: str = "de"
    ) -> Dict:
        city = city or self.city_name
        if not city:
            raise ValueError("CITY_NAME must be set in settings.py")

        params = {"q": city, "units": units, "lang": lang}

        return self._make_request("weather", params)

    def validate_api_key(self) -> bool:
        try:
            self.get_current_weather("London")
            return True
        except requests.RequestException:
            return False

    def get_icon_url(self, icon_code: str, size: str = "2x") -> str:
        return f"https://openweathermap.org/img/wn/{icon_code}@{size}.png"
