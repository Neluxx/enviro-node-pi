from django.core.management.base import BaseCommand

from pi_sensor.services import SensorReader, SensorRepository


class Command(BaseCommand):
    help = "Collect sensor data from sensors on the raspberry pi"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sensor_reader = SensorReader()
        self.repository = SensorRepository()

    def handle(self, *args, **kwargs) -> None:
        sensor_data = self.sensor_reader.collect_data()
        self.repository.insert(sensor_data)
