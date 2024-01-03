from django.core.management.base import BaseCommand
from apps.sensor.services import Sensor


class Command(BaseCommand):
    help = "Get sensor data"

    def handle(self, *args, **kwargs):
        sensor = Sensor()
        sensor_data = sensor.get_data()
        sensor.save_data(sensor_data)
