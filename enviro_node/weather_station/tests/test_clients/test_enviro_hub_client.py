from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from requests.exceptions import HTTPError, RequestException
from weather_station.clients.enviro_hub_client import EnviroHubClient


class EnviroHubClientTest(TestCase):

    @override_settings(BASE_URL="https://example.com/api", BEARER_TOKEN="test")
    def test_initialization_sets_correct_base_url(self) -> None:
        client = EnviroHubClient()

        self.assertEqual(client.base_url, "https://example.com/api")

    @override_settings(BASE_URL="https://example.com/api", BEARER_TOKEN="test")
    def test_initialization_sets_correct_headers(self) -> None:
        client = EnviroHubClient()

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
    def test_submit_data_calls_correct_url(
        self,
        mock_return_json: Mock,
        mock_make_request: Mock,
    ) -> None:
        client = EnviroHubClient()
        mock_response = Mock()
        mock_make_request.return_value = mock_response
        mock_return_json.return_value = {"status": "success"}

        data = [{"temperature": 22.5, "humidity": 45.0}]
        client.submit_data("/sensor-data", data)

        mock_make_request.assert_called_once_with(
            "POST",
            "https://example.com/api/sensor-data",
            json_data=data,
            verify=False,
        )

    @patch.object(EnviroHubClient, "_make_http_request")
    @patch.object(EnviroHubClient, "_return_json_response")
    @override_settings(BASE_URL="https://example.com/api", BEARER_TOKEN="test")
    def test_submit_data_handles_trailing_slashes(
        self,
        mock_return_json: Mock,
        mock_make_request: Mock,
    ) -> None:
        client = EnviroHubClient()
        mock_response = Mock()
        mock_make_request.return_value = mock_response
        mock_return_json.return_value = {"status": "success"}

        data = [{"temperature": 22.5}]
        client.submit_data("/sensor-data", data)

        mock_make_request.assert_called_once_with(
            "POST",
            "https://example.com/api/sensor-data",
            json_data=data,
            verify=False,
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
        expected_response = {"status": "success", "records_created": 5}
        mock_return_json.return_value = expected_response

        data = [{"temperature": 22.5}]
        result = client.submit_data("/sensor-data", data)

        self.assertEqual(result, expected_response)
        mock_return_json.assert_called_once_with(mock_response)

    @patch.object(EnviroHubClient, "_make_http_request")
    @override_settings(BASE_URL="https://example.com/api", BEARER_TOKEN="test")
    def test_submit_data_with_empty_list(
        self,
        mock_make_request: Mock,
    ) -> None:
        client = EnviroHubClient()
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_make_request.return_value = mock_response

        data = []
        result = client.submit_data("/sensor-data", data)

        mock_make_request.assert_called_once_with(
            "POST",
            "https://example.com/api/sensor-data",
            json_data=[],
            verify=False,
        )
        self.assertIsInstance(result, dict)

    @patch.object(EnviroHubClient, "_make_http_request")
    @override_settings(BASE_URL="https://example.com/api", BEARER_TOKEN="test")
    def test_submit_data_with_multiple_records(
        self,
        mock_make_request: Mock,
    ) -> None:
        client = EnviroHubClient()
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_make_request.return_value = mock_response

        data = [
            {"temperature": 22.5, "humidity": 45.0},
            {"temperature": 23.0, "humidity": 46.0},
            {"temperature": 21.8, "humidity": 44.5},
        ]
        client.submit_data("/sensor-data", data)

        mock_make_request.assert_called_once()
        args, kwargs = mock_make_request.call_args
        self.assertEqual(kwargs["json_data"], data)
        self.assertEqual(len(kwargs["json_data"]), 3)

    @patch.object(EnviroHubClient, "_make_http_request")
    @override_settings(BASE_URL="https://example.com/api", BEARER_TOKEN="test")
    def test_submit_data_propagates_http_errors(
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
    def test_submit_data_propagates_request_exceptions(
        self,
        mock_make_request: Mock,
    ) -> None:
        client = EnviroHubClient()
        mock_make_request.side_effect = RequestException("Connection error")

        data = [{"temperature": 22.5}]

        with self.assertRaises(RequestException):
            client.submit_data("/sensor-data", data)
