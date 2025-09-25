from typing import Any

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

TEMPERATURE_VALIDATORS = [MinValueValidator(-100), MaxValueValidator(100)]
PERCENTAGE_VALIDATORS = [MinValueValidator(0), MaxValueValidator(100)]  # In percentage
PRESSURE_VALIDATORS = [MinValueValidator(900), MaxValueValidator(1100)]  # In hPa
VISIBILITY_VALIDATORS = [MinValueValidator(0), MaxValueValidator(10000)]  # In meter
WIND_SPEED_VALIDATORS = [MinValueValidator(0), MaxValueValidator(150)]  # In m/s
WIND_DEGREE_VALIDATORS = [MinValueValidator(0), MaxValueValidator(360)]  # In degree


class OutdoorWeatherData(models.Model):
    temperature = models.FloatField(validators=TEMPERATURE_VALIDATORS)
    feels_like = models.FloatField(validators=TEMPERATURE_VALIDATORS)
    temp_min = models.FloatField(validators=TEMPERATURE_VALIDATORS)
    temp_max = models.FloatField(validators=TEMPERATURE_VALIDATORS)
    humidity = models.IntegerField(validators=PERCENTAGE_VALIDATORS)
    pressure = models.IntegerField(validators=PRESSURE_VALIDATORS)

    weather_main = models.CharField(max_length=255, blank=False)
    weather_description = models.CharField(max_length=255, blank=False)
    weather_icon = models.CharField(max_length=255, blank=False)

    visibility = models.IntegerField(validators=VISIBILITY_VALIDATORS)
    wind_speed = models.FloatField(validators=WIND_SPEED_VALIDATORS)
    wind_deg = models.IntegerField(validators=WIND_DEGREE_VALIDATORS)
    clouds = models.IntegerField(validators=PERCENTAGE_VALIDATORS)

    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def to_dict(self) -> dict:
        """Return model data as a dictionary with JSON-serializable datetime strings"""
        return {
            "temperature": self.temperature,
            "feels_like": self.feels_like,
            "temp_min": self.temp_min,
            "temp_max": self.temp_max,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "weather_main": self.weather_main,
            "weather_description": self.weather_description,
            "weather_icon": self.weather_icon,
            "visibility": self.visibility,
            "wind_speed": self.wind_speed,
            "wind_deg": self.wind_deg,
            "clouds": self.clouds,
            "created_at": self.created_at.isoformat(),
        }
