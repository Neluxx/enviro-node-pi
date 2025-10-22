from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from weather_station.models import IndoorSensorData
from weather_station.services import SensorReader


class SensorDataCollectorTestCase(TestCase):
    def test_handle_collects_and_stores_sensor_data_successfully(self) -> None:
        initial_count = IndoorSensorData.objects.count()

        with self.assertLogs("weather_station", level="INFO") as cm:
            call_command("sensor_data_collector", stdout=StringIO())

        self.assertEqual(IndoorSensorData.objects.count(), initial_count + 1)

        record = IndoorSensorData.objects.latest("created_at")
        self.assertTrue(20.0 <= record.temperature <= 24.0)
        self.assertTrue(40.0 <= record.humidity <= 50.0)
        self.assertTrue(1003.25 <= record.pressure <= 1023.25)
        self.assertTrue(400.0 <= record.co2 <= 800.0)
        self.assertIsNone(record.submitted_at)

        self.assertIn("Starting sensor data collection", cm.output[0])
        self.assertIn("Collecting sensor data...", cm.output[1])
        self.assertIn("Read data from bme680:", cm.output[2])
        self.assertIn("Read data from mhz19:", cm.output[3])
        self.assertIn("Collected sensor data:", cm.output[4])
        self.assertIn("Storing sensor data to database...", cm.output[5])
        self.assertIn("Sensor data collection completed successfully", cm.output[6])

    @patch.object(SensorReader, "collect_data")
    def test_handle_logs_error_when_sensor_reader_fails(
        self, mock_collect_data
    ) -> None:
        initial_count = IndoorSensorData.objects.count()
        mock_collect_data.side_effect = RuntimeError("Sensor connection failed")

        with self.assertLogs("weather_station", level="INFO") as cm:
            with self.assertRaises(RuntimeError):
                call_command("sensor_data_collector", stdout=StringIO())

        self.assertEqual(IndoorSensorData.objects.count(), initial_count)

        self.assertIn("Starting sensor data collection", cm.output[0])
        self.assertIn("Collecting sensor data...", cm.output[1])
        self.assertIn("Error during sensor data collection:", cm.output[2])
        self.assertIn("Sensor connection failed", cm.output[2])
        self.assertIn("Sensor data collection completed successfully", cm.output[3])
