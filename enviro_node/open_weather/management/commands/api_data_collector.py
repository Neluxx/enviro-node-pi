from typing import Any
from django.core.management.base import BaseCommand
from open_weather.services import OpenWeather


class Command(BaseCommand):
    help = "Get open weather data"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        open_weather = OpenWeather()
        open_weather_data = open_weather.get_data()
        open_weather.save_data(open_weather_data)
