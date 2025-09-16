from django.core.management.base import BaseCommand

from open_weather.services import OpenWeatherClient, OpenWeatherRepository


class Command(BaseCommand):
    help = "Get open weather data"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.open_weather_client = OpenWeatherClient()
        self.repository = OpenWeatherRepository()

    def handle(self, *args, **kwargs) -> None:
        open_weather_data = self.open_weather_client.get_current_weather()
        self.repository.insert(open_weather_data)
