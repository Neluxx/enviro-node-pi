from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class OutdoorWeatherData(models.Model):
    temperature = models.FloatField(
        validators=[MinValueValidator(-100), MaxValueValidator(70)]
    )
    feels_like = models.FloatField(
        validators=[MinValueValidator(-100), MaxValueValidator(70)]
    )
    temp_min = models.FloatField(
        validators=[MinValueValidator(-100), MaxValueValidator(70)]
    )
    temp_max = models.FloatField(
        validators=[MinValueValidator(-100), MaxValueValidator(70)]
    )
    humidity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    pressure = models.IntegerField(
        validators=[MinValueValidator(500), MaxValueValidator(1200)]
    )

    weather_main = models.CharField(max_length=255, blank=False)
    weather_description = models.CharField(max_length=255, blank=False)
    weather_icon = models.CharField(max_length=255, blank=False)

    visibility = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50000)]
    )
    wind_speed = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    wind_deg = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(360)]
    )
    clouds = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "OpenWeather-Data"
        verbose_name_plural = "OpenWeather-Data"

    def __str__(self) -> str:
        date_str = self.created_at.strftime("%d.%m.%Y %H:%M")
        return f"{self.weather_main} - {self.temperature}°C ({date_str})"

    def clean(self) -> None:
        super().clean()

        if self.temp_min is not None and self.temp_max is not None:
            if self.temp_min > self.temp_max:
                raise ValidationError(
                    {
                        "temp_min": (
                            "The minimum temperature cannot be "
                            "higher than the maximum temperature."
                        ),
                        "temp_max": (
                            "The maximum temperature cannot be "
                            "lower than the minimum temperature."
                        ),
                    }
                )

        if self.temperature is not None:
            if self.temp_min is not None and self.temperature < self.temp_min:
                raise ValidationError(
                    {
                        "temperature": (
                            "The current temperature cannot be "
                            "lower than the minimum temperature."
                        )
                    }
                )
            if self.temp_max is not None and self.temperature > self.temp_max:
                raise ValidationError(
                    {
                        "temperature": (
                            "The current temperature cannot be "
                            "higher than the maximum temperature."
                        )
                    }
                )

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
