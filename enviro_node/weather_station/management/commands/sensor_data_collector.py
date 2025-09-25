import logging

from django.core.management.base import BaseCommand

from weather_station.services import SensorReader, SensorRepository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Collect sensor data from raspberry pi sensors"

    def handle(self, *args, **kwargs) -> None:
        logger.info("Starting sensor data collection")

        try:
            logger.info("Collecting sensor data...")
            sensor_data = SensorReader().collect_data()
            logger.info(f"Collected sensor data: {sensor_data}")

            logger.info("Storing sensor data to database...")
            SensorRepository().insert(sensor_data)

        except Exception as e:
            logger.error(f"Error during sensor data collection: {e}")
            raise

        finally:
            logger.info("Sensor data collection completed successfully")
