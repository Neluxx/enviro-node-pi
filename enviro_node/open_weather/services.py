import requests
import logging

from django.conf import settings

from .models import OutdoorWeatherData


class OpenWeather:
    """Open Weather Class"""

    def __init__(self) -> None:
        self.api_key = settings.API_KEY
        self.city_name = settings.CITY_NAME

    def get_data(self) -> dict:
        """Get response from open weather map"""

        if self.api_key is None or self.city_name is None:
            raise NameError("Der API Key oder die Stadt fehlt.")

        base_url: str = "https://api.openweathermap.org/data/2.5/weather"
        params: dict[str, str] = {
            "q": self.city_name,
            "appid": self.api_key,
            "units": "metric",
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()

            data: dict = response.json()

            if data:
                return data

        except requests.RequestException as exception:
            logging.error("Fehler bei der Anfrage:", exception)

        return {}

    def save_data(self, data: dict) -> None:
        OutdoorWeatherData(
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            temp_min=data["main"]["temp_min"],
            temp_max=data["main"]["temp_max"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            weather_main=data["weather"][0]["main"],
            weather_description=data["weather"][0]["description"],
            weather_icon=data["weather"][0]["icon"],
            visibility=data["visibility"],
            wind_speed=data["wind"]["speed"],
            wind_deg=data["wind"]["deg"],
            clouds=data["clouds"]["all"],
        ).save()
