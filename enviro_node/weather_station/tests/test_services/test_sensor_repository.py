from django.test import TestCase
from django.utils import timezone

from weather_station.models import IndoorSensorData
from weather_station.services import SensorRepository


class SensorRepositoryTest(TestCase):
    fixtures = ["sensor_data.json"]

    def setUp(self) -> None:
        self.repository = SensorRepository()
        self.valid_data = {
            "temperature": 22.5,
            "humidity": 45.0,
            "pressure": 1013.25,
            "co2": 400.0,
        }

    def test_find_unsubmitted_data_returns_empty_queryset(self) -> None:
        IndoorSensorData.objects.all().delete()

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

        record1 = IndoorSensorData.objects.get(pk=1)
        record2 = IndoorSensorData.objects.get(pk=2)
        record3 = IndoorSensorData.objects.get(pk=3)

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
        initial_count = IndoorSensorData.objects.count()

        self.repository.insert(self.valid_data)

        self.assertEqual(IndoorSensorData.objects.count(), initial_count + 1)

        record = IndoorSensorData.objects.latest("created_at")
        self.assertEqual(float(record.temperature), self.valid_data["temperature"])
        self.assertEqual(float(record.humidity), self.valid_data["humidity"])
        self.assertEqual(float(record.pressure), self.valid_data["pressure"])
        self.assertEqual(float(record.co2), self.valid_data["co2"])
        self.assertIsNone(record.submitted_at)

    def test_insert_does_not_create_record_when_missing_temperature(self) -> None:
        invalid_data = self.valid_data.copy()
        del invalid_data["temperature"]
        initial_count = IndoorSensorData.objects.count()

        with self.assertLogs("weather_station.services", level="WARNING") as cm:
            self.repository.insert(invalid_data)

        self.assertEqual(IndoorSensorData.objects.count(), initial_count)
        self.assertIn("Missing required sensor field: 'temperature'", cm.output[0])

    def test_insert_does_not_create_record_when_missing_humidity(self) -> None:
        invalid_data = self.valid_data.copy()
        del invalid_data["humidity"]
        initial_count = IndoorSensorData.objects.count()

        with self.assertLogs("weather_station.services", level="WARNING") as cm:
            self.repository.insert(invalid_data)

        self.assertEqual(IndoorSensorData.objects.count(), initial_count)
        self.assertIn("Missing required sensor field: 'humidity'", cm.output[0])

    def test_insert_does_not_create_record_when_missing_pressure(self) -> None:
        invalid_data = self.valid_data.copy()
        del invalid_data["pressure"]
        initial_count = IndoorSensorData.objects.count()

        with self.assertLogs("weather_station.services", level="WARNING") as cm:
            self.repository.insert(invalid_data)

        self.assertEqual(IndoorSensorData.objects.count(), initial_count)
        self.assertIn("Missing required sensor field: 'pressure'", cm.output[0])

    def test_insert_does_not_create_record_when_missing_co2(self) -> None:
        invalid_data = self.valid_data.copy()
        del invalid_data["co2"]
        initial_count = IndoorSensorData.objects.count()

        with self.assertLogs("weather_station.services", level="WARNING") as cm:
            self.repository.insert(invalid_data)

        self.assertEqual(IndoorSensorData.objects.count(), initial_count)
        self.assertIn("Missing required sensor field: 'co2'", cm.output[0])

    def test_insert_does_not_create_record_when_invalid_temperature(self) -> None:
        invalid_data = self.valid_data.copy()
        invalid_data["temperature"] = "invalid"
        initial_count = IndoorSensorData.objects.count()

        with self.assertLogs("weather_station.services", level="ERROR") as cm:
            self.repository.insert(invalid_data)

        self.assertEqual(IndoorSensorData.objects.count(), initial_count)
        self.assertIn("Sensor data validation failed:", cm.output[0])
        self.assertIn("temperature", cm.output[0])

    def test_insert_does_not_create_record_when_invalid_humidity(self) -> None:
        invalid_data = self.valid_data.copy()
        invalid_data["humidity"] = "invalid"
        initial_count = IndoorSensorData.objects.count()

        with self.assertLogs("weather_station.services", level="ERROR") as cm:
            self.repository.insert(invalid_data)

        self.assertEqual(IndoorSensorData.objects.count(), initial_count)
        self.assertIn("Sensor data validation failed:", cm.output[0])
        self.assertIn("humidity", cm.output[0])

    def test_insert_does_not_create_record_when_invalid_pressure(self) -> None:
        invalid_data = self.valid_data.copy()
        invalid_data["pressure"] = "invalid"
        initial_count = IndoorSensorData.objects.count()

        with self.assertLogs("weather_station.services", level="ERROR") as cm:
            self.repository.insert(invalid_data)

        self.assertEqual(IndoorSensorData.objects.count(), initial_count)
        self.assertIn("Sensor data validation failed:", cm.output[0])
        self.assertIn("pressure", cm.output[0])

    def test_insert_does_not_create_record_when_invalid_co2(self) -> None:
        invalid_data = self.valid_data.copy()
        invalid_data["co2"] = "invalid"
        initial_count = IndoorSensorData.objects.count()

        with self.assertLogs("weather_station.services", level="ERROR") as cm:
            self.repository.insert(invalid_data)

        self.assertEqual(IndoorSensorData.objects.count(), initial_count)
        self.assertIn("Sensor data validation failed:", cm.output[0])
        self.assertIn("co2", cm.output[0])

    def test_insert_does_not_create_record_with_empty_dict(self) -> None:
        initial_count = IndoorSensorData.objects.count()

        with self.assertLogs("weather_station.services", level="WARNING") as cm:
            self.repository.insert({})

        self.assertEqual(IndoorSensorData.objects.count(), initial_count)
        self.assertIn("Missing required sensor field: 'temperature'", cm.output[0])