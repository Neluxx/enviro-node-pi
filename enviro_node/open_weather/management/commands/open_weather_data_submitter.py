from django.core.management.base import BaseCommand

from enviro_hub.services.enviro_hub_client import submit_data
from open_weather.services import OpenWeatherReader


class Command(BaseCommand):
    help = "Get open weather data"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.open_weather_reader = OpenWeatherReader()

    def handle(self, *args, **kwargs) -> None:
        queryset = self.open_weather_reader.get_unsubmitted_data()
        open_weather_data = [obj.to_dict() for obj in queryset]
        submit_data("/open-weather-data", open_weather_data)
        self.open_weather_reader.mark_as_submitted(queryset)
