from django.db.models import QuerySet
from django.utils import timezone

from open_weather.models import OutdoorWeatherData


class OpenWeatherReader:

    def get_unsubmitted_data(self) -> QuerySet[OutdoorWeatherData]:
        return OutdoorWeatherData.objects.filter(submitted_at=None).order_by(
            "created_at"
        )

    def mark_as_submitted(self, queryset: QuerySet[OutdoorWeatherData]) -> int:
        return queryset.update(submitted_at=timezone.now())
