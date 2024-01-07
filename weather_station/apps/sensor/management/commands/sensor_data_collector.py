from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from apps.sensor.services import Sensor


class Command(BaseCommand):
    help = "Get sensor data"

    def handle(self, *args, **kwargs):
        sensor = Sensor()
        sensor_data = sensor.get_data()
        sensor.save_data(sensor_data)

        if sensor_data["co2"] >= 1200:
            self.send_mail(sensor_data)

    def send_mail(self, sensor_data: dict) -> None:
        send_mail(
            "Luftqualität ist schlecht",
            f'Die CO2-Konzentration in der Luft beträgt {sensor_data["co2"]}. Es wird Zeit zu lüften.',
            "fabian.arndt96@proton.me",
            ["fabian.arndt96@proton.me"],
            fail_silently=False,
        )
