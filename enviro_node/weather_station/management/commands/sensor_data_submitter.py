import logging

from django.core.management.base import BaseCommand

from weather_station.clients import EnviroHubClient
from weather_station.services import SensorRepository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Submit raspberry pi sensor data to enviro hub"

    BATCH_SIZE = 1000

    def handle(self, *args, **kwargs) -> None:
        logger.info("Starting sensor data submission")

        try:
            total_submitted = 0

            while True:
                logger.info("Find unsubmitted sensor data...")
                queryset = SensorRepository().find_unsubmitted_data()[: self.BATCH_SIZE]

                if not queryset.exists():
                    logger.info("No unsubmitted sensor data found")
                    break

                logger.info(f"Found {queryset.count()} unsubmitted record(s)")
                sensor_data = [obj.to_dict() for obj in queryset]
                logger.info(f"Unsubmitted sensor data: {sensor_data}")

                logger.info("Submit sensor data to enviro hub...")
                EnviroHubClient().submit_data("/environmental-data", sensor_data)
                logger.info("Sensor data successfully submitted")

                logger.info("Mark sensor data as submitted...")
                record_ids = [obj.id for obj in queryset]
                updated_count = SensorRepository().mark_as_submitted(record_ids)
                logger.info(f"Marked {updated_count} record(s) as submitted")

                total_submitted += updated_count

            logger.info(f"Total records submitted: {total_submitted}")

        except Exception as e:
            logger.error(f"Error during sensor data submission: {e}")
            raise

        finally:
            logger.info("Finished sensor data submission")
