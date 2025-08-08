from django.test import TestCase
from unittest.mock import patch
from .models import OutdoorWeatherData
from .services import OpenWeather


class OpenWeatherTest(TestCase):
    def setUp(self):
        self.open_weather = OpenWeather()
        self.mock_response = {
            "main": {
                "temp": 20,
                "feels_like": 21,
                "temp_min": 15,
                "temp_max": 25,
                "pressure": 1012,
                "humidity": 80,
            },
            "weather": [
                {"main": "Clouds", "description": "overcast clouds", "icon": "04n"}
            ],
            "visibility": 10000,
            "wind": {"speed": 5.1, "deg": 350},
            "clouds": {"all": 90},
            "dt": 1605182400,
        }

    @patch("open_weather.services.requests.get")
    def test_get_data(self, mock_get):
        # Mocking der HTTP-Anfrage
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_response

        data = self.open_weather.get_data()
        self.assertEqual(data, self.mock_response)

    @patch("open_weather.services.requests.get")
    def test_save_data(self, mock_get):
        # Mocking der HTTP-Anfrage
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_response

        data = self.open_weather.get_data()
        self.open_weather.save_data(data)

        # Überprüfen, ob die Daten korrekt in der Datenbank gespeichert wurden
        self.assertEqual(OutdoorWeatherData.objects.count(), 1)
        saved_data = OutdoorWeatherData.objects.first()
        self.assertEqual(saved_data.temperature, 20)
        self.assertEqual(saved_data.humidity, 80)
        # ... (Überprüfe alle anderen Felder entsprechend)

    @patch("open_weather.services.requests.get")
    def test_api_error_handling(self, mock_get):
        # Simulieren eines Fehlers bei der API-Anfrage
        mock_get.side_effect = Exception("API-Anfrage fehlgeschlagen")

        with self.assertRaises(Exception):
            self.open_weather.get_data()
