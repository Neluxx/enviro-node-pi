from django.db import models


class IndoorSensorData(models.Model):
    temperature = models.DecimalField(max_digits=15, decimal_places=2)
    humidity = models.DecimalField(max_digits=15, decimal_places=2)
    pressure = models.DecimalField(max_digits=15, decimal_places=2)
    co2 = models.DecimalField(max_digits=15, decimal_places=2)
    created = models.DateTimeField()
