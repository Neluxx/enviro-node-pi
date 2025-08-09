from unittest.mock import patch

from django.test import TestCase

from pi_sensor.sensors.FakeBME680 import FakeBME680Sensor
from pi_sensor.sensors.FakeMHZ19 import FakeMHZ19Sensor
from pi_sensor.sensors.sensor_factory import SensorFactory


class TestSensorFactory(TestCase):

    @patch("pi_sensor.sensors.sensor_factory.settings.MOCK_SENSORS", True)
    def test_create_bme680_sensor_returns_fake_sensor(self) -> None:
        sensor = SensorFactory.create_bme680_sensor()
        self.assertIsInstance(sensor, FakeBME680Sensor)

    @patch("pi_sensor.sensors.sensor_factory.settings.MOCK_SENSORS", True)
    def test_create_mhz19_sensor_returns_fake_sensor(self) -> None:
        sensor = SensorFactory.create_mhz19_sensor()
        self.assertIsInstance(sensor, FakeMHZ19Sensor)
