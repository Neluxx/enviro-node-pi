from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from weather_station.models import IndoorSensorData


class SensorDataSubmitterTestCase(TestCase):
    fixtures = ["sensor_data.json"]

    def test_handle_reset_sensor_data_successfully(self) -> None:
        record1 = IndoorSensorData.objects.get(pk=1)
        record2 = IndoorSensorData.objects.get(pk=2)

        self.assertIsNotNone(record1.submitted_at)
        self.assertIsNotNone(record2.submitted_at)

        with self.assertLogs("weather_station", level="INFO") as cm:
            call_command("sensor_data_resetter", stdout=StringIO())

        record1 = IndoorSensorData.objects.get(pk=1)
        record2 = IndoorSensorData.objects.get(pk=2)

        self.assertIsNone(record1.submitted_at)
        self.assertIsNone(record2.submitted_at)

        expected_logs = [
            "Resetting sensor data",
            "Find submitted sensor data...",
            "Found 2 submitted record(s)",
            "Mark sensor data as unsubmitted...",
            "Marked 2 record(s) as unsubmitted",
            "Find submitted sensor data...",
            "No submitted sensor data found",
            "Total records resetted: 2",
            "Finished resetting sensor data",
        ]

        for i, expected_log in enumerate(expected_logs):
            self.assertIn(expected_log, cm.output[i])
