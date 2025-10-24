from typing import Any

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

TEMPERATURE_VALIDATORS = [MinValueValidator(-100), MaxValueValidator(100)]
PERCENTAGE_VALIDATORS = [MinValueValidator(0), MaxValueValidator(100)]  # In percentage
PRESSURE_VALIDATORS = [MinValueValidator(900), MaxValueValidator(1100)]  # In hPa
CO2_VALIDATORS = [MinValueValidator(300), MaxValueValidator(5000)]  # In ppm


class IndoorSensorData(models.Model):
    temperature = models.FloatField(validators=TEMPERATURE_VALIDATORS)
    humidity = models.FloatField(validators=PERCENTAGE_VALIDATORS)
    pressure = models.FloatField(validators=PRESSURE_VALIDATORS)
    co2 = models.FloatField(validators=CO2_VALIDATORS, null=True, blank=True)

    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def to_dict(self) -> dict:
        """Return model data as a dictionary with JSON-serializable datetime strings"""
        result = {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "created_at": timezone.localtime(self.created_at).isoformat(),
        }

        if self.co2 is not None:
            result["co2"] = self.co2

        return result
