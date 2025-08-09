from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase


class TestSensorDataCollector(TestCase):
    def setUp(self) -> None:
        self.patcher_reader = patch(
            "pi_sensor.services.sensor_data_reader.SensorDataReader.get_data"
        )
        self.patcher_saver = patch(
            "pi_sensor.services.sensor_data_saver.SensorDataSaver.save_data"
        )
        self.mock_reader = self.patcher_reader.start()
        self.mock_saver = self.patcher_saver.start()

    def tearDown(self) -> None:
        self.patcher_reader.stop()
        self.patcher_saver.stop()

    @patch(
        "pi_sensor.services.sensor_data_reader.SensorDataReader.get_data",
        return_value={
            "temperature": 22.5,
            "humidity": 50.0,
            "pressure": 1015.0,
            "co2": 400.0,
        },
    )
    @patch("pi_sensor.services.sensor_data_saver.SensorDataSaver.save_data")
    def test_handle_calls_reader_and_saver(
        self, mock_saver: MagicMock, mock_reader: MagicMock
    ) -> None:
        call_command("sensor_data_collector")
        self.assertTrue(mock_reader.called)
        self.assertTrue(mock_saver.called)

    @patch(
        "pi_sensor.services.sensor_data_reader.SensorDataReader.get_data",
        return_value={
            "temperature": 22.5,
            "humidity": 50.0,
            "pressure": 1015.0,
            "co2": 400.0,
        },
    )
    @patch("pi_sensor.services.sensor_data_saver.SensorDataSaver.save_data")
    def test_handle_passes_data_correctly(
        self, mock_saver: MagicMock, mock_reader: MagicMock
    ) -> None:
        call_command("sensor_data_collector")
        mock_saver.assert_called_once_with(
            {
                "temperature": 22.5,
                "humidity": 50.0,
                "pressure": 1015.0,
                "co2": 400.0,
            }
        )

    @patch(
        "pi_sensor.services.sensor_data_reader.SensorDataReader.get_data",
        return_value={},
    )
    @patch("pi_sensor.services.sensor_data_saver.SensorDataSaver.save_data")
    def test_handle_handles_empty_data(
        self, mock_saver: MagicMock, mock_reader: MagicMock
    ) -> None:
        call_command("sensor_data_collector")
        mock_saver.assert_called_once_with({})
