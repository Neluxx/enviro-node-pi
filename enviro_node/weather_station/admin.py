from django.contrib import admin

from weather_station.models import IndoorSensorData, OutdoorWeatherData

admin.site.register(IndoorSensorData)
admin.site.register(OutdoorWeatherData)
