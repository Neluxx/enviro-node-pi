from typing import Any

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class IndoorSensorData(models.Model):
    temperature = models.FloatField(
        validators=[MinValueValidator(-40), MaxValueValidator(85)]
    )
    humidity = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    pressure = models.FloatField(
        validators=[MinValueValidator(300), MaxValueValidator(1100)]
    )
    co2 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def to_dict(self) -> dict:
        """Return model data as a dictionary with JSON-serializable datetime strings"""
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "co2": self.co2,
            "created_at": self.created_at.isoformat(),
        }
