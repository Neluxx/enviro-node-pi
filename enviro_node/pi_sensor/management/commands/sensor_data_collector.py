import logging

from django.core.management.base import BaseCommand

from pi_sensor.services import SensorReader, SensorRepository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Collect sensor data from raspberry pi sensors"

    def handle(self, *args, **kwargs) -> None:
        logger.info("Starting sensor data collection")

        try:
            sensor_reader = SensorReader()
            repository = SensorRepository()

            logger.info("Collecting sensor data...")
            sensor_data = sensor_reader.collect_data()
            logger.info(f"Collected sensor data: {sensor_data}")

            logger.info("Storing sensor data to database...")
            repository.insert(sensor_data)
            logger.info("Sensor data collection completed successfully")

        except Exception as e:
            logger.error(f"Error during sensor data collection: {e}")
            raise

        finally:
            logger.info("Finished sensor data collection")
