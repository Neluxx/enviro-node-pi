import logging

from django.core.management.base import BaseCommand

from weather_station.clients import EnviroHubClient
from weather_station.services import OpenWeatherRepository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Submit open weather data to enviro hub"

    BATCH_SIZE = 1000

    def handle(self, *args, **kwargs) -> None:
        logger.info("Starting open weather data submission")

        try:
            total_submitted = 0

            while True:
                logger.info("Find unsubmitted open weather data...")
                queryset = OpenWeatherRepository().find_unsubmitted_data()[
                    : self.BATCH_SIZE
                ]

                if not queryset.exists():
                    logger.info("No unsubmitted open weather data found")
                    break

                logger.info(f"Found {queryset.count()} unsubmitted record(s)")
                open_weather_data = [obj.to_dict() for obj in queryset]
                logger.info(f"Unsubmitted open weather data: {open_weather_data}")

                logger.info("Submit open weather data to enviro hub...")
                EnviroHubClient().submit_data("/open-weather-data", open_weather_data)
                logger.info("Open weather data successfully submitted")

                logger.info("Mark open weather data as submitted...")
                record_ids = [obj.id for obj in queryset]
                updated_count = OpenWeatherRepository().mark_as_submitted(record_ids)
                logger.info(f"Marked {updated_count} record(s) as submitted")

                total_submitted += updated_count

            logger.info(f"Total records submitted: {total_submitted}")

        except Exception as e:
            logger.error(f"Error during open weather data submission: {e}")
            raise

        finally:
            logger.info("Finished open weather data submission")
