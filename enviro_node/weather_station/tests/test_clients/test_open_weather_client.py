from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from requests.exceptions import HTTPError, RequestException
from weather_station.clients.open_weather_client import OpenWeatherClient


class OpenWeatherClientTest(TestCase):

    @override_settings(API_KEY="test", CITY_NAME="Zurich")
    def test_initialization(self) -> None:
        client = OpenWeatherClient()

        self.assertEqual(client.api_key, "test")
        self.assertEqual(client.city_name, "Zurich")

    @override_settings(API_KEY="test", CITY_NAME="Zurich")
    @patch.object(OpenWeatherClient, "_make_http_request")
    @patch.object(OpenWeatherClient, "_return_json_response")
    def test_get_current_weather_returns_json_response(
        self,
        mock_return_json: Mock,
        mock_make_request: Mock,
    ) -> None:
        client = OpenWeatherClient()
        mock_response = Mock()
        mock_make_request.return_value = mock_response
        expected_response = {
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
        mock_return_json.return_value = expected_response

        result = client.get_current_weather()

        self.assertEqual(result, expected_response)
        mock_return_json.assert_called_once_with(mock_response)
        mock_make_request.assert_called_once_with(
            "GET",
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": "Zurich",
                "appid": "test",
                "units": "metric",
                "lang": "de",
            },
        )

    @override_settings(API_KEY="test", CITY_NAME="Zurich")
    @patch.object(OpenWeatherClient, "_make_http_request")
    def test_get_current_weather_raises_http_errors(
        self,
        mock_make_request: Mock,
    ) -> None:
        client = OpenWeatherClient()
        mock_make_request.side_effect = HTTPError("401 Unauthorized")

        with self.assertRaises(HTTPError):
            client.get_current_weather()

    @override_settings(API_KEY="test", CITY_NAME="Zurich")
    @patch.object(OpenWeatherClient, "_make_http_request")
    def test_get_current_weather_raises_request_exceptions(
        self,
        mock_make_request: Mock,
    ) -> None:
        client = OpenWeatherClient()
        mock_make_request.side_effect = RequestException("Connection timeout")

        with self.assertRaises(RequestException):
            client.get_current_weather()
