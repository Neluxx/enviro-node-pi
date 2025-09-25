import logging

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.utils import timezone

from weather_station.models import IndoorSensorData

logger = logging.getLogger(__name__)


class SensorRepository:

    def find_unsubmitted_data(self) -> QuerySet[IndoorSensorData]:
        return IndoorSensorData.objects.filter(submitted_at=None).order_by("created_at")

    def mark_as_submitted(self, queryset: QuerySet[IndoorSensorData]) -> int:
        return queryset.update(submitted_at=timezone.now())

    def insert(self, data: dict[str, float]) -> None:
        try:
            IndoorSensorData(
                temperature=data["temperature"],
                humidity=data["humidity"],
                pressure=data["pressure"],
                co2=data["co2"],
            ).save()
        except KeyError as e:
            logger.warning(f"Missing required sensor field: {e}")
        except ValidationError as e:
            logger.error(f"Sensor data validation failed: {e}")
