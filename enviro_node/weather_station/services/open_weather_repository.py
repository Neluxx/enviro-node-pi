import logging

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.utils import timezone

from weather_station.models import OutdoorWeatherData

logger = logging.getLogger(__name__)


class OpenWeatherRepository:

    def find_unsubmitted_data(self) -> QuerySet[OutdoorWeatherData]:
        return OutdoorWeatherData.objects.filter(submitted_at=None).order_by(
            "created_at"
        )

    def mark_as_submitted(self, ids: list[int]) -> int:
        return OutdoorWeatherData.objects.filter(id__in=ids).update(
            submitted_at=timezone.now()
        )

    def insert(self, data: dict) -> None:
        try:
            OutdoorWeatherData(
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                temp_min=data["main"]["temp_min"],
                temp_max=data["main"]["temp_max"],
                humidity=data["main"]["humidity"],
                pressure=data["main"]["pressure"],
                weather_main=data["weather"][0]["main"],
                weather_description=data["weather"][0]["description"],
                weather_icon=data["weather"][0]["icon"],
                visibility=data["visibility"],
                wind_speed=data["wind"]["speed"],
                wind_deg=data["wind"]["deg"],
                clouds=data["clouds"]["all"],
            ).save()
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
        except ValidationError as e:
            logger.error(f"Data validation failed: {e}")
