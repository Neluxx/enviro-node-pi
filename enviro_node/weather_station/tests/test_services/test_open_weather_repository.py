from typing import Any

from django.test import TestCase
from django.utils import timezone

from weather_station.models import OutdoorWeatherData
from weather_station.services import OpenWeatherRepository


class SensorRepositoryTest(TestCase):
    fixtures = ["weather_data.json"]

    def setUp(self) -> None:
        self.repository = OpenWeatherRepository()
        self.valid_data: dict[str, Any] = {
            "main": {
                "temp": 19.5,
                "feels_like": 19.1,
                "temp_min": 18.3,
                "temp_max": 20.4,
                "humidity": 62,
                "pressure": 1016,
            },
            "weather": [
                {
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d",
                }
            ],
            "visibility": 10000,
            "wind": {
                "speed": 3.2,
                "deg": 240,
            },
            "clouds": {
                "all": 20,
            },
        }

    def test_find_unsubmitted_data_returns_empty_queryset(self) -> None:
        OutdoorWeatherData.objects.all().delete()

        result = self.repository.find_unsubmitted_data()

        self.assertEqual(result.count(), 0)

    def test_find_unsubmitted_data_returns_unsubmitted_records(self) -> None:
        result = self.repository.find_unsubmitted_data()

        self.assertEqual(result.count(), 3)
        for record in result:
            self.assertIsNone(record.submitted_at)

        result_ids = [r.id for r in result]
        self.assertIn(3, result_ids)
        self.assertIn(4, result_ids)
        self.assertIn(5, result_ids)

    def test_find_unsubmitted_data_ordered_by_created_at(self) -> None:
        result = list(self.repository.find_unsubmitted_data())

        self.assertEqual(result[0].id, 3)
        self.assertEqual(result[1].id, 4)
        self.assertEqual(result[2].id, 5)

    def test_mark_as_submitted_updates_records_with_ids(self) -> None:
        ids_to_submit = [1, 2]

        before_update = timezone.now()
        updated_count = self.repository.mark_as_submitted(ids_to_submit)
        after_update = timezone.now()

        self.assertEqual(updated_count, 2)

        record1 = OutdoorWeatherData.objects.get(pk=1)
        record2 = OutdoorWeatherData.objects.get(pk=2)
        record3 = OutdoorWeatherData.objects.get(pk=3)

        self.assertIsNotNone(record1.submitted_at)
        self.assertIsNotNone(record2.submitted_at)
        self.assertIsNone(record3.submitted_at)

        assert record1.submitted_at is not None
        assert record2.submitted_at is not None

        self.assertGreaterEqual(record1.submitted_at, before_update)
        self.assertLessEqual(record1.submitted_at, after_update)
        self.assertGreaterEqual(record2.submitted_at, before_update)
        self.assertLessEqual(record2.submitted_at, after_update)

    def test_mark_as_submitted_returns_zero_when_no_matching_ids(self) -> None:
        non_existent_ids = [9999, 10000]

        updated_count = self.repository.mark_as_submitted(non_existent_ids)

        self.assertEqual(updated_count, 0)

    def test_mark_as_submitted_with_empty_list(self) -> None:
        updated_count = self.repository.mark_as_submitted([])

        self.assertEqual(updated_count, 0)

    def test_insert_creates_record_with_valid_data(self) -> None:
        initial_count = OutdoorWeatherData.objects.count()

        self.repository.insert(self.valid_data)

        self.assertEqual(OutdoorWeatherData.objects.count(), initial_count + 1)

        record = OutdoorWeatherData.objects.latest("created_at")
        self.assertEqual(float(record.temperature), self.valid_data["main"]["temp"])
        self.assertEqual(
            float(record.feels_like), self.valid_data["main"]["feels_like"]
        )
        self.assertEqual(float(record.temp_min), self.valid_data["main"]["temp_min"])
        self.assertEqual(float(record.temp_max), self.valid_data["main"]["temp_max"])
        self.assertEqual(int(record.humidity), self.valid_data["main"]["humidity"])
        self.assertEqual(int(record.pressure), self.valid_data["main"]["pressure"])
        self.assertEqual(
            str(record.weather_main), self.valid_data["weather"][0]["main"]
        )
        self.assertEqual(
            str(record.weather_description),
            self.valid_data["weather"][0]["description"],
        )
        self.assertEqual(
            str(record.weather_icon), self.valid_data["weather"][0]["icon"]
        )
        self.assertEqual(int(record.visibility), self.valid_data["visibility"])
        self.assertEqual(float(record.wind_speed), self.valid_data["wind"]["speed"])
        self.assertEqual(int(record.wind_deg), self.valid_data["wind"]["deg"])
        self.assertEqual(int(record.clouds), self.valid_data["clouds"]["all"])
        self.assertIsNone(record.submitted_at)

    def test_insert_does_not_create_record_when_missing_temperature(self) -> None:
        invalid_data = {
            "main": {
                "feels_like": 19.1,
                "temp_min": 18.3,
                "temp_max": 20.4,
                "humidity": 62,
                "pressure": 1016,
            },
            "weather": [
                {
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d",
                }
            ],
            "visibility": 10000,
            "wind": {
                "speed": 3.2,
                "deg": 240,
            },
            "clouds": {
                "all": 20,
            },
        }
        initial_count = OutdoorWeatherData.objects.count()

        self.repository.insert(invalid_data)

        self.assertEqual(OutdoorWeatherData.objects.count(), initial_count)

    def test_insert_does_not_create_record_when_missing_humidity(self) -> None:
        invalid_data = {
            "main": {
                "temp": 19.5,
                "feels_like": 19.1,
                "temp_min": 18.3,
                "temp_max": 20.4,
                "pressure": 1016,
            },
            "weather": [
                {
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d",
                }
            ],
            "visibility": 10000,
            "wind": {
                "speed": 3.2,
                "deg": 240,
            },
            "clouds": {
                "all": 20,
            },
        }
        initial_count = OutdoorWeatherData.objects.count()

        self.repository.insert(invalid_data)

        self.assertEqual(OutdoorWeatherData.objects.count(), initial_count)

    def test_insert_does_not_create_record_when_missing_pressure(self) -> None:
        invalid_data = {
            "main": {
                "temp": 19.5,
                "feels_like": 19.1,
                "temp_min": 18.3,
                "temp_max": 20.4,
                "humidity": 62,
            },
            "weather": [
                {
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d",
                }
            ],
            "visibility": 10000,
            "wind": {
                "speed": 3.2,
                "deg": 240,
            },
            "clouds": {
                "all": 20,
            },
        }
        initial_count = OutdoorWeatherData.objects.count()

        self.repository.insert(invalid_data)

        self.assertEqual(OutdoorWeatherData.objects.count(), initial_count)

    def test_insert_does_not_create_record_with_empty_dict(self) -> None:
        initial_count = OutdoorWeatherData.objects.count()

        self.repository.insert({})

        self.assertEqual(OutdoorWeatherData.objects.count(), initial_count)
