import logging

from django.core.management.base import BaseCommand

from open_weather.services import OpenWeatherClient, OpenWeatherRepository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Retrieve current weather data from open weather API"

    def handle(self, *args, **kwargs) -> None:
        logger.info("Starting open weather data retrieving")

        try:
            logger.info("Retrieve current open weather data...")
            open_weather_data = OpenWeatherClient().get_current_weather()
            logger.info(f"Retrieved current open weather data: {open_weather_data}")

            logger.info("Storing open weather data to database...")
            OpenWeatherRepository().insert(open_weather_data)

        except Exception as e:
            logger.error(f"Error during open weather data retrieving: {e}")
            raise

        finally:
            logger.info("Open weather data retrieving completed successfully")
