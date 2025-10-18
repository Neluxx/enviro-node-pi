from django.test import TestCase

from weather_station.services.sensor_factory import SensorType
from weather_station.services.sensor_reader import SensorReader


class SensorReaderTest(TestCase):
    def setUp(self) -> None:
        self.reader = SensorReader()

    def test_initialize_sensors(self) -> None:
        self.assertIsInstance(self.reader.sensors, dict)
        self.assertEqual(len(self.reader.sensors), len(SensorType))
        for sensor_type in SensorType:
            self.assertIn(sensor_type, self.reader.sensors)

    def test_collect_data_returns_valid_structure(self) -> None:
        with self.assertLogs("weather_station.services", level="INFO") as cm:
            data = self.reader.collect_data()

        self.assertIn("Read data from bme680", cm.output[0])
        self.assertIn("Read data from mhz19", cm.output[1])

        self.assertIsInstance(data, dict)
        self.assertIn("temperature", data)
        self.assertIn("humidity", data)
        self.assertIn("pressure", data)
        self.assertIn("co2", data)

        expected_keys = ["temperature", "humidity", "pressure", "co2"]
        self.assertCountEqual(data.keys(), expected_keys)

        self.assertIsInstance(data["temperature"], float)
        self.assertIsInstance(data["humidity"], float)
        self.assertIsInstance(data["pressure"], float)
        self.assertIsInstance(data["co2"], float)

    def test_collect_data_fake_sensor_values(self) -> None:
        with self.assertLogs("weather_station.services", level="INFO") as cm:
            data = self.reader.collect_data()

        self.assertIn("Read data from bme680", cm.output[0])
        self.assertIn("Read data from mhz19", cm.output[1])

        self.assertTrue(20.0 <= data["temperature"] <= 24.0)
        self.assertTrue(40.0 <= data["humidity"] <= 50.0)
        self.assertTrue(1003.25 <= data["pressure"] <= 1023.25)
        self.assertTrue(400.0 <= data["co2"] <= 800.0)

    def test_collect_data_raises_error_when_no_sensors_available(self) -> None:
        reader = SensorReader()
        reader.sensors = {}

        with self.assertRaises(RuntimeError) as context:
            reader.collect_data()

        self.assertEqual(str(context.exception), "No sensors available")
