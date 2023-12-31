from django.db import models


class OutdoorWeatherData(models.Model):
    temperature = models.DecimalField(max_digits=15, decimal_places=2)
    feels_like = models.DecimalField(max_digits=15, decimal_places=2)
    temp_min = models.DecimalField(max_digits=15, decimal_places=2)
    temp_max = models.DecimalField(max_digits=15, decimal_places=2)
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    weather_main = models.CharField(max_length=255)
    weather_description = models.CharField(max_length=255)
    weather_icon = models.CharField(max_length=255)
    visibility = models.IntegerField()
    wind_speed = models.DecimalField(max_digits=15, decimal_places=2)
    wind_deg = models.IntegerField()
    clouds = models.IntegerField()
    created = models.DateTimeField()
