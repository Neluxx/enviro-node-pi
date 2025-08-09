from unittest.mock import MagicMock

from django.test import TestCase

from pi_sensor.services.sensor_data_reader import SensorDataReader


class TestSensorDataReader(TestCase):

    def setUp(self) -> None:
        self.mock_bme680_sensor = MagicMock()
        self.mock_mhz19_sensor = MagicMock()
        self.reader = SensorDataReader()
        self.reader.bme680_sensor = self.mock_bme680_sensor
        self.reader.mhz19_sensor = self.mock_mhz19_sensor

    def test_get_data_returns_combined_data(self) -> None:
        self.mock_bme680_sensor.get_data.return_value = {
            "temperature": 22.5,
            "humidity": 45.0,
        }
        self.mock_mhz19_sensor.get_data.return_value = {"co2": 400.0}

        expected_data = {"temperature": 22.5, "humidity": 45.0, "co2": 400.0}
        actual_data = self.reader.get_data()

        self.assertEqual(expected_data, actual_data)

    def test_get_data_handles_empty_sensor_data(self) -> None:
        self.mock_bme680_sensor.get_data.return_value = {}
        self.mock_mhz19_sensor.get_data.return_value = {}

        expected_data: dict = {}
        actual_data = self.reader.get_data()

        self.assertEqual(expected_data, actual_data)

    def test_get_data_handles_partial_data(self) -> None:
        self.mock_bme680_sensor.get_data.return_value = {"temperature": 22.5}
        self.mock_mhz19_sensor.get_data.return_value = {}

        expected_data = {"temperature": 22.5}
        actual_data = self.reader.get_data()

        self.assertEqual(expected_data, actual_data)

    def test_get_data_calls_both_sensors(self) -> None:
        self.mock_bme680_sensor.get_data.return_value = {"temperature": 22.5}
        self.mock_mhz19_sensor.get_data.return_value = {"co2": 400.0}

        self.reader.get_data()

        self.mock_bme680_sensor.get_data.assert_called_once()
        self.mock_mhz19_sensor.get_data.assert_called_once()
