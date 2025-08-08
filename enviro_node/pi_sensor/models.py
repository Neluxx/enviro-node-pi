from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class IndoorSensorData(models.Model):
    temperature = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(-40), MaxValueValidator(85)],
    )
    humidity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    pressure = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(300), MaxValueValidator(1100)],
    )
    co2 = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5000)],
    )
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Innenraum-Sensordaten"
        verbose_name_plural = "Innenraum-Sensordaten"
