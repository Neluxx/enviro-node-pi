import logging

from django.core.management.base import BaseCommand

from weather_station.services import OpenWeatherRepository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Reset open weather data"

    BATCH_SIZE = 1000

    def handle(self, *args, **kwargs) -> None:
        logger.info("Resetting open weather data")

        try:
            total_resetted = 0

            while True:
                logger.info("Find submitted open weather data...")
                queryset = OpenWeatherRepository().find_submitted_data()[
                    : self.BATCH_SIZE
                ]

                if not queryset.exists():
                    logger.info("No submitted open weather data found")
                    break

                logger.info(f"Found {queryset.count()} submitted record(s)")
                record_ids = [obj.id for obj in queryset]

                logger.info("Mark open weather data as unsubmitted...")
                updated_count = OpenWeatherRepository().mark_as_unsubmitted(record_ids)
                logger.info(f"Marked {updated_count} record(s) as unsubmitted")

                total_resetted += updated_count

            logger.info(f"Total records resetted: {total_resetted}")

        except Exception as e:
            logger.error(f"Error during open weather data reset: {e}")
            raise

        finally:
            logger.info("Finished resetting open weather data")
