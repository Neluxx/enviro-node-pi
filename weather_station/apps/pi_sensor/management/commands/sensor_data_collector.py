from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from apps.pi_sensor.services import Sensor
from apps.pi_sensor.models import IndoorSensorData


class Command(BaseCommand):
    help = 'Get pi_sensor data'

    def handle(self, *args, **kwargs):
        sensor = Sensor()
        actual_sensor_data = sensor.get_data()
        last_sensor_data = IndoorSensorData.objects.latest('created')
        sensor.save_data(actual_sensor_data)

        if actual_sensor_data['co2'] >= 1000 and last_sensor_data.co2 < 1000:
            self.send_warning_mail(actual_sensor_data)

        if actual_sensor_data['co2'] < 1000 and last_sensor_data.co2 >= 1000:
            self.send_recovery_mail()

    def send_warning_mail(self, actual_sensor_data: dict) -> None:
        send_mail(
            'Luftqualität ist schlecht',
            f'Die CO2-Konzentration in der Luft beträgt {actual_sensor_data['co2']}. Es wird Zeit zu lüften.',
            'mail@fabian-arndt.dev',
            ['fabian.arndt96@proton.me', 'sukathrin@web.de'],
            fail_silently=False,
        )

    def send_recovery_mail(self) -> None:
        send_mail(
            'Luftqualität hat sich verbessert',
            'Die CO2-Konzentration ist unter den Schwellenwert gesunken. Du kannst die Fenster wieder schliessen.',
            'mail@fabian-arndt.dev',
            ['fabian.arndt96@proton.me', 'sukathrin@web.de'],
            fail_silently=False,
        )
