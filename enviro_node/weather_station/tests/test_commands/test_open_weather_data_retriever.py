from io import StringIO
from typing import Any
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from weather_station.clients import OpenWeatherClient
from weather_station.models import OutdoorWeatherData


class OpenWeatherDataRetrieverTestCase(TestCase):
    def setUp(self) -> None:
        self.valid_weather_data: dict[str, Any] = {
            "main": {
                "temp": 20.5,
                "feels_like": 19.8,
                "temp_min": 18.0,
                "temp_max": 22.0,
                "humidity": 65,
                "pressure": 1015,
            },
            "weather": [
                {
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d",
                }
            ],
            "visibility": 10000,
            "wind": {"speed": 3.5, "deg": 180},
            "clouds": {"all": 20},
        }

    @patch.object(OpenWeatherClient, "get_current_weather")
    def test_handle_retrieves_and_stores_weather_data_successfully(
        self, mock_get_weather
    ) -> None:
        mock_get_weather.return_value = self.valid_weather_data
        initial_count = OutdoorWeatherData.objects.count()

        with self.assertLogs("weather_station", level="INFO") as cm:
            call_command("open_weather_data_retriever", stdout=StringIO())

        self.assertEqual(OutdoorWeatherData.objects.count(), initial_count + 1)

        record = OutdoorWeatherData.objects.latest("created_at")
        self.assertEqual(float(record.temperature), 20.5)
        self.assertEqual(float(record.feels_like), 19.8)
        self.assertEqual(float(record.temp_min), 18.0)
        self.assertEqual(float(record.temp_max), 22.0)
        self.assertEqual(int(record.humidity), 65)
        self.assertEqual(int(record.pressure), 1015)
        self.assertEqual(str(record.weather_main), "Clouds")
        self.assertEqual(str(record.weather_description), "few clouds")
        self.assertEqual(str(record.weather_icon), "02d")
        self.assertEqual(int(record.visibility), 10000)
        self.assertEqual(float(record.wind_speed), 3.5)
        self.assertEqual(int(record.wind_deg), 180)
        self.assertEqual(int(record.clouds), 20)
        self.assertIsNone(record.submitted_at)

        self.assertIn("Starting open weather data retrieving", cm.output[0])
        self.assertIn("Retrieve current open weather data...", cm.output[1])
        self.assertIn("Retrieved current open weather data:", cm.output[2])
        self.assertIn("Storing open weather data to database...", cm.output[3])
        self.assertIn(
            "Open weather data retrieving completed successfully", cm.output[4]
        )

    @patch.object(OpenWeatherClient, "get_current_weather")
    def test_handle_logs_error_when_client_fails(self, mock_get_weather) -> None:
        initial_count = OutdoorWeatherData.objects.count()
        mock_get_weather.side_effect = RuntimeError("API connection failed")

        with self.assertLogs("weather_station", level="INFO") as cm:
            with self.assertRaises(RuntimeError):
                call_command("open_weather_data_retriever", stdout=StringIO())

        self.assertEqual(OutdoorWeatherData.objects.count(), initial_count)

        self.assertIn("Starting open weather data retrieving", cm.output[0])
        self.assertIn("Retrieve current open weather data...", cm.output[1])
        self.assertIn("Error during open weather data retrieving:", cm.output[2])
        self.assertIn("API connection failed", cm.output[2])
        self.assertIn(
            "Open weather data retrieving completed successfully", cm.output[3]
        )
