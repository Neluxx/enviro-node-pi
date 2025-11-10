import logging

from django.core.management.base import BaseCommand

from weather_station.services import SensorRepository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Reset raspberry pi sensor data"

    BATCH_SIZE = 1000

    def handle(self, *args, **kwargs) -> None:
        logger.info("Resetting sensor data")

        try:
            total_resetted = 0

            while True:
                logger.info("Find submitted sensor data...")
                queryset = SensorRepository().find_submitted_data()[: self.BATCH_SIZE]

                if not queryset.exists():
                    logger.info("No submitted sensor data found")
                    break

                logger.info(f"Found {queryset.count()} submitted record(s)")
                record_ids = [obj.id for obj in queryset]

                logger.info("Mark sensor data as unsubmitted...")
                updated_count = SensorRepository().mark_as_unsubmitted(record_ids)
                logger.info(f"Marked {updated_count} record(s) as unsubmitted")

                total_resetted += updated_count

            logger.info(f"Total records resetted: {total_resetted}")

        except Exception as e:
            logger.error(f"Error during sensor data reset: {e}")
            raise

        finally:
            logger.info("Finished resetting sensor data")
