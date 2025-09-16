from xml.dom import ValidationErr

from django.db.models import QuerySet
from django.utils import timezone

from open_weather.models import OutdoorWeatherData


class OpenWeatherRepository:

    def find_unsubmitted_data(self) -> QuerySet[OutdoorWeatherData]:
        return OutdoorWeatherData.objects.filter(submitted_at=None).order_by(
            "created_at"
        )

    def mark_as_submitted(self, queryset: QuerySet[OutdoorWeatherData]) -> int:
        return queryset.update(submitted_at=timezone.now())

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
        except KeyError:
            pass
        except ValidationErr:
            pass
