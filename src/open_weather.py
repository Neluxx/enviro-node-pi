#!/usr/bin/env python3
"""
Open Weather Map
"""

import os
import requests


class OpenWeather:
    """Open Weather Class"""

    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")
        self.city_name = os.getenv("CITY_NAME")

    def get_data(self) -> dict:
        """Get response from open weather map"""

        if self.api_key is None or self.city_name is None:
            raise NameError("Der API Key oder die Stadt fehlt.")

        base_url: str = "https://api.openweathermap.org/data/2.5/weather"
        params: dict = {
            "q": self.city_name,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()

            data: dict = response.json()

            if data:
                return data

        except requests.RequestException as exception:
            print("Fehler bei der Anfrage:", exception)

        return {}
