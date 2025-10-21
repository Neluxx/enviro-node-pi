from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from requests.exceptions import HTTPError, RequestException
from weather_station.clients.enviro_hub_client import EnviroHubClient


class EnviroHubClientTest(TestCase):

    @override_settings(BASE_URL="https://example.com/api", BEARER_TOKEN="test")
    def test_initialization(self) -> None:
        client = EnviroHubClient()

        self.assertEqual(client.base_url, "https://example.com/api")
        self.assertEqual(
            client.session.headers["Authorization"],
            "Bearer test",
        )
        self.assertEqual(
            client.session.headers["Content-Type"],
            "application/json",
        )
        self.assertEqual(
            client.session.headers["Accept"],
            "application/json",
        )

    @patch.object(EnviroHubClient, "_make_http_request")
    @patch.object(EnviroHubClient, "_return_json_response")
    @override_settings(BASE_URL="https://example.com/api", BEARER_TOKEN="test")
    def test_submit_data_returns_json_response(
        self,
        mock_return_json: Mock,
        mock_make_request: Mock,
    ) -> None:
        client = EnviroHubClient()
        mock_response = Mock()
        mock_make_request.return_value = mock_response
        expected_response = {"status": "success"}
        mock_return_json.return_value = expected_response

        data = [
            {"temperature": 22.5, "humidity": 45.0},
            {"temperature": 23.0, "humidity": 46.0},
            {"temperature": 21.8, "humidity": 44.5},
        ]
        result = client.submit_data("/sensor-data", data)

        self.assertEqual(result, expected_response)
        mock_make_request.assert_called_once_with(
            "POST",
            "https://example.com/api/sensor-data",
            json_data=data,
            verify=False,
        )

    @patch.object(EnviroHubClient, "_make_http_request")
    @override_settings(BASE_URL="https://example.com/api", BEARER_TOKEN="test")
    def test_submit_data_raises_http_errors(
        self,
        mock_make_request: Mock,
    ) -> None:
        client = EnviroHubClient()
        mock_make_request.side_effect = HTTPError("404 Not Found")

        data = [{"temperature": 22.5}]

        with self.assertRaises(HTTPError):
            client.submit_data("/sensor-data", data)

    @patch.object(EnviroHubClient, "_make_http_request")
    @override_settings(BASE_URL="https://example.com/api", BEARER_TOKEN="test")
    def test_submit_data_raises_request_exceptions(
        self,
        mock_make_request: Mock,
    ) -> None:
        client = EnviroHubClient()
        mock_make_request.side_effect = RequestException("Connection error")

        data = [{"temperature": 22.5}]

        with self.assertRaises(RequestException):
            client.submit_data("/sensor-data", data)
