from typing import Dict

from django.conf import settings

from common.services import BaseHttpClient


class OpenWeatherClient(BaseHttpClient):

    def __init__(self) -> None:
        super().__init__()
        self.api_key = settings.API_KEY
        self.city_name = settings.CITY_NAME

    def get_current_weather(self) -> Dict:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": self.city_name,
            "appid": self.api_key,
            "units": "metric",
            "lang": "de",
        }
        response = self._make_http_request("GET", url, params=params)

        return self._return_json_response(response)
