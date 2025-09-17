from django.core.management.base import BaseCommand

from enviro_hub.services.enviro_hub_client import submit_data
from open_weather.services import OpenWeatherRepository


class Command(BaseCommand):
    help = "Submit open weather data to the enviro hub"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.repository = OpenWeatherRepository()

    def handle(self, *args, **kwargs) -> None:
        queryset = self.repository.find_unsubmitted_data()
        open_weather_data = [obj.to_dict() for obj in queryset]
        submit_data("/open-weather-data", open_weather_data)
        self.repository.mark_as_submitted(queryset)
