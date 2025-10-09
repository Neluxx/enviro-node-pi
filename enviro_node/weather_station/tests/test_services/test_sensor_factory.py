from django.test import TestCase, override_settings

from weather_station.sensors.fake_bme680 import FakeBME680Sensor
from weather_station.sensors.fake_mh_z19 import FakeMHZ19Sensor
from weather_station.services.sensor_factory import SensorFactory, SensorType


class SensorFactoryTestCase(TestCase):

    @override_settings(MOCK_SENSORS=True)
    def test_create_fake_bme680_sensor(self) -> None:
        sensor = SensorFactory.create_sensor(SensorType.BME680)

        self.assertIsInstance(sensor, FakeBME680Sensor)
        self.assertTrue(hasattr(sensor, "get_data"))
        self.assertTrue(callable(sensor.get_data))

    @override_settings(MOCK_SENSORS=True)
    def test_create_fake_mhz19_sensor(self) -> None:
        sensor = SensorFactory.create_sensor(SensorType.MHZ19)

        self.assertIsInstance(sensor, FakeMHZ19Sensor)
        self.assertTrue(hasattr(sensor, "get_data"))
        self.assertTrue(callable(sensor.get_data))

    @override_settings(MOCK_SENSORS=True)
    def test_fake_sensors_return_valid_data(self) -> None:
        bme680 = SensorFactory.create_sensor(SensorType.BME680)
        mhz19 = SensorFactory.create_sensor(SensorType.MHZ19)

        bme680_data = bme680.get_data()
        mhz19_data = mhz19.get_data()

        self.assertIsInstance(bme680_data, dict)
        self.assertIn("temperature", bme680_data)
        self.assertIn("humidity", bme680_data)
        self.assertIn("pressure", bme680_data)
        self.assertIsInstance(bme680_data["temperature"], float)
        self.assertIsInstance(bme680_data["humidity"], float)
        self.assertIsInstance(bme680_data["pressure"], float)

        self.assertIsInstance(mhz19_data, dict)
        self.assertIn("co2", mhz19_data)
        self.assertIsInstance(mhz19_data["co2"], float)
