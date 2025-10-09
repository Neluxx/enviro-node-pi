from django.test import TestCase

from weather_station.sensors.fake_mh_z19 import FakeMHZ19Sensor


class FakeMHZ19SensorTest(TestCase):
    def setUp(self) -> None:
        self.sensor = FakeMHZ19Sensor()

    def test_get_data_returns_valid_structure(self) -> None:
        data = self.sensor.get_data()

        self.assertIsInstance(data, dict)
        self.assertIn("co2", data)
        self.assertCountEqual(data.keys(), ["co2"])

    def test_get_data_value_is_float_and_in_expected_range(self) -> None:
        data = self.sensor.get_data()

        self.assertIsInstance(data["co2"], float)
        self.assertTrue(400.0 <= data["co2"] <= 800.0)
