import logging

from django.core.management.base import BaseCommand

from weather_station.clients import EnviroHubClient
from weather_station.services import SensorRepository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Submit raspberry pi sensor data to enviro hub"

    def handle(self, *args, **kwargs) -> None:
        logger.info("Starting sensor data submission")

        try:
            logger.info("Find unsubmitted sensor data...")
            queryset = SensorRepository().find_unsubmitted_data()
            if not queryset.exists():
                logger.info("No unsubmitted sensor data found")
                return

            logger.info(f"Found {queryset.count()} unsubmitted record(s)")
            sensor_data = [obj.to_dict() for obj in queryset]
            logger.info(f"Unsubmitted sensor data: {sensor_data}")

            logger.info("Submit sensor data to enviro hub...")
            EnviroHubClient().submit_data("/environmental-data", sensor_data)
            logger.info("Sensor data successfully submitted")

            logger.info("Mark sensor data as submitted...")
            updated_count = SensorRepository().mark_as_submitted(queryset)
            logger.info(f"Marked {updated_count} record(s) as submitted")

        except Exception as e:
            logger.error(f"Error during sensor data submission: {e}")
            raise

        finally:
            logger.info("Finished sensor data submission")
