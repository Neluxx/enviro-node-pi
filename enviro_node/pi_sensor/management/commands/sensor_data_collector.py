from django.core.management.base import BaseCommand

from pi_sensor.services import SensorDataReader, SensorDataRepository


class Command(BaseCommand):
    help = "Get pi_sensor data"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sensor_reader = SensorDataReader()
        self.repository = SensorDataRepository()

    def handle(self, *args, **kwargs) -> None:
        sensor_data = self.sensor_reader.get_data()
        self.repository.insert(sensor_data)
