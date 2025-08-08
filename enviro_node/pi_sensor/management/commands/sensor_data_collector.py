from typing import Any
from django.core.management.base import BaseCommand

from pi_sensor.services import SensorDataReader, SensorDataSaver


class Command(BaseCommand):
    help = "Get pi_sensor data"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.sensor_reader = SensorDataReader()
        self.sensor_saver = SensorDataSaver()

    def handle(self, *args: Any, **kwargs: Any) -> None:
        sensor_data = self.sensor_reader.get_data()
        self.sensor_saver.save_data(sensor_data)
