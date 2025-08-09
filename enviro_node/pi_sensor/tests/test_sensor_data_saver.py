from unittest.mock import MagicMock, patch
from xml.dom import ValidationErr

from django.test import TestCase

from pi_sensor.services.sensor_data_saver import SensorDataSaver


class TestSensorDataSaver(TestCase):
    def setUp(self) -> None:
        self.saver = SensorDataSaver()

    @patch("pi_sensor.models.IndoorSensorData.save")
    def test_save_data_saves_valid_data_correctly(self, mock_save: MagicMock) -> None:
        data = {
            "temperature": 22.5,
            "humidity": 50.0,
            "pressure": 1015.0,
            "co2": 400.0,
        }
        self.saver.save_data(data)
        self.assertTrue(mock_save.called)

    @patch("pi_sensor.models.IndoorSensorData.save")
    def test_save_data_raises_validation_error(self, mock_save: MagicMock) -> None:
        mock_save.side_effect = ValidationErr("Invalid data")
        data = {
            "temperature": 22.5,
            "humidity": 150.0,
            "pressure": 1015.0,
            "co2": 400.0,
        }
        self.saver.save_data(data)
        self.assertTrue(mock_save.called)

    @patch("pi_sensor.models.IndoorSensorData.save")
    def test_save_data_handles_missing_fields(self, mock_save: MagicMock) -> None:
        data = {
            "temperature": 22.5,
            "humidity": 50.0,
            "pressure": 1015.0,
        }
        self.saver.save_data(data)
        self.assertFalse(mock_save.called)

    @patch("pi_sensor.models.IndoorSensorData.save")
    def test_save_data_handles_empty_data(self, mock_save: MagicMock) -> None:
        data: dict = {}
        self.saver.save_data(data)
        self.assertFalse(mock_save.called)
