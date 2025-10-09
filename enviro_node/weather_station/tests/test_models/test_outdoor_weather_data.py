from django.test import TestCase

from weather_station.models.outdoor_weather_data import OutdoorWeatherData


class OutdoorWeatherDataTestCase(TestCase):
    fixtures = ["weather_data.json"]

    def test_to_dict_returns_expected_dict(self) -> None:
        result = OutdoorWeatherData.objects.get(pk=1).to_dict()

        self.assertEqual(
            result,
            {
                "temperature": 15.3,
                "feels_like": 14.2,
                "temp_min": 13.8,
                "temp_max": 16.5,
                "humidity": 72,
                "pressure": 1013,
                "weather_main": "Clouds",
                "weather_description": "scattered clouds",
                "weather_icon": "03d",
                "visibility": 10000,
                "wind_speed": 3.5,
                "wind_deg": 180,
                "clouds": 40,
                "created_at": "2025-10-03T10:00:00+02:00",
            },
        )
