from xml.dom import ValidationErr

from django.db.models import QuerySet
from django.utils import timezone

from pi_sensor.models import IndoorSensorData


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
        except KeyError:
            pass
        except ValidationErr:
            pass
