from django.core.management.base import BaseCommand

from enviro_hub.services.enviro_hub_client import submit_data
from pi_sensor.services import SensorRepository


class Command(BaseCommand):
    help = "Submit sensor data to the enviro hub"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.repository = SensorRepository()

    def handle(self, *args, **kwargs) -> None:
        queryset = self.repository.find_unsubmitted_data()
        sensor_data = [obj.to_dict() for obj in queryset]
        submit_data("/environmental-data", sensor_data)
        self.repository.mark_as_submitted(queryset)
