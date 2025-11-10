from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from weather_station.models import OutdoorWeatherData


class OpenWeatherDataSubmitterTestCase(TestCase):
    fixtures = ["weather_data.json"]

    def test_handle_reset_open_weather_data_successfully(self) -> None:
        record1 = OutdoorWeatherData.objects.get(pk=1)
        record2 = OutdoorWeatherData.objects.get(pk=2)

        self.assertIsNotNone(record1.submitted_at)
        self.assertIsNotNone(record2.submitted_at)

        with self.assertLogs("weather_station", level="INFO") as cm:
            call_command("open_weather_data_resetter", stdout=StringIO())

        record1 = OutdoorWeatherData.objects.get(pk=1)
        record2 = OutdoorWeatherData.objects.get(pk=2)

        self.assertIsNone(record1.submitted_at)
        self.assertIsNone(record2.submitted_at)

        expected_logs = [
            "Resetting open weather data",
            "Find submitted open weather data...",
            "Found 2 submitted record(s)",
            "Mark open weather data as unsubmitted...",
            "Marked 2 record(s) as unsubmitted",
            "Find submitted open weather data...",
            "No submitted open weather data found",
            "Total records resetted: 2",
            "Finished resetting open weather data",
        ]

        for i, expected_log in enumerate(expected_logs):
            self.assertIn(expected_log, cm.output[i])
