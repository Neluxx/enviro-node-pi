from django.test import TestCase

from weather_station.models.indoor_sensor_data import IndoorSensorData


class IndoorSensorDataTestCase(TestCase):
    fixtures = ["sensor_data.json"]

    def test_to_dict_returns_expected_dict(self) -> None:
        result = IndoorSensorData.objects.get(pk=1).to_dict()

        self.assertEqual(
            result,
            {
                "temperature": 20.3,
                "humidity": 54.7,
                "pressure": 1013.8,
                "co2": 456.9,
                "created_at": "2025-10-03T10:00:00+02:00",
            },
        )
