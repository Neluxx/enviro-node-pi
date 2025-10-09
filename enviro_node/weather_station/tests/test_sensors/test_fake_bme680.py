from django.test import TestCase

from weather_station.sensors.fake_bme680 import FakeBME680Sensor


class FakeBME680SensorTest(TestCase):
    def setUp(self) -> None:
        self.sensor = FakeBME680Sensor()

    def test_get_data_returns_valid_structure(self) -> None:
        data = self.sensor.get_data()

        self.assertIsInstance(data, dict)
        self.assertIn("temperature", data)
        self.assertIn("humidity", data)
        self.assertIn("pressure", data)
        self.assertCountEqual(data.keys(), ["temperature", "humidity", "pressure"])

    def test_get_data_values_are_floats_and_in_expected_ranges(self) -> None:
        data = self.sensor.get_data()

        self.assertIsInstance(data["temperature"], float)
        self.assertIsInstance(data["humidity"], float)
        self.assertIsInstance(data["pressure"], float)
        self.assertTrue(20.0 <= data["temperature"] <= 24.0)
        self.assertTrue(40.0 <= data["humidity"] <= 50.0)
        self.assertTrue(1003.25 <= data["pressure"] <= 1023.25)
