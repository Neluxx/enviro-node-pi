from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from weather_station.clients import EnviroHubClient
from weather_station.models import IndoorSensorData


class SensorDataSubmitterTestCase(TestCase):
    fixtures = ["sensor_data.json"]

    @patch.object(EnviroHubClient, "submit_data")
    def test_handle_submits_sensor_data_successfully(self, mock_submit_data) -> None:
        mock_submit_data.return_value = {"status": "success"}

        with self.assertLogs("weather_station", level="INFO") as cm:
            call_command("sensor_data_submitter", stdout=StringIO())

        mock_submit_data.assert_called_once()
        args, kwargs = mock_submit_data.call_args
        self.assertEqual(args[0], "/sensor-data")
        submitted_data = args[1]
        self.assertEqual(len(submitted_data), 3)

        record3 = IndoorSensorData.objects.get(pk=3)
        record4 = IndoorSensorData.objects.get(pk=4)
        record5 = IndoorSensorData.objects.get(pk=5)

        self.assertIsNotNone(record3.submitted_at)
        self.assertIsNotNone(record4.submitted_at)
        self.assertIsNotNone(record5.submitted_at)

        expected_logs = [
            "Starting sensor data submission",
            "Find unsubmitted sensor data...",
            "Found 3 unsubmitted record(s)",
            "Unsubmitted sensor data:",
            "Submit sensor data to enviro hub...",
            "Sensor data successfully submitted",
            "Mark sensor data as submitted...",
            "Marked 3 record(s) as submitted",
            "Find unsubmitted sensor data...",
            "No unsubmitted sensor data found",
            "Total records submitted: 3",
            "Finished sensor data submission",
        ]

        for i, expected_log in enumerate(expected_logs):
            self.assertIn(expected_log, cm.output[i])

    @patch.object(EnviroHubClient, "submit_data")
    def test_handle_logs_error_when_client_fails(self, mock_submit_data) -> None:
        mock_submit_data.side_effect = RuntimeError("API connection failed")

        with self.assertLogs("weather_station", level="INFO") as cm:
            with self.assertRaises(RuntimeError):
                call_command("sensor_data_submitter", stdout=StringIO())

        self.assertIn("Starting sensor data submission", cm.output[0])
        self.assertIn("Find unsubmitted sensor data...", cm.output[1])
        self.assertIn("Found 3 unsubmitted record(s)", cm.output[2])
        self.assertIn("Unsubmitted sensor data:", cm.output[3])
        self.assertIn("Submit sensor data to enviro hub...", cm.output[4])
        self.assertIn("Error during sensor data submission:", cm.output[5])
        self.assertIn("API connection failed", cm.output[5])
        self.assertIn("Finished sensor data submission", cm.output[6])
