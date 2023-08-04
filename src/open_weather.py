#!/usr/bin/env python3
"""
Open Weather Map
"""

import os
import requests


class OpenWeather:
    """Open Weather Class"""

    def __init__(self):
        self.api_key = os.getenv("API_KEY")

    def get_sea_level_pressure(self):
        """Get response from open weather map"""

        city_name = "Münchenstein,Switzerland"
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city_name, "appid": self.api_key}

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                sea_level_pressure = data["main"]["sea_level"]
                return sea_level_pressure

            else:
                print("Fehler beim Abrufen der Daten. Statuscode:", response.status_code)
                return None

        except requests.RequestException as exception:
            print("Fehler bei der Anfrage:", exception)
            return None
