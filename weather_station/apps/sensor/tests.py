from django.test import TestCase
from unittest.mock import patch, MagicMock
from apps.sensor.models import IndoorSensorData
from apps.sensor.services import Sensor


@patch('apps.sensor.services.mh_z19', MagicMock())
@patch('apps.sensor.services.bme680', MagicMock())
class SensorTest(TestCase):
    def setUp(self):
        # Konfigurieren der Mock-Objekte
        self.mh_z19_mock = MagicMock()
        self.mh_z19_mock = {'co2': 400.0}

        self.bme680_sensor_mock = MagicMock()
        self.bme680_sensor_mock.data.temperature = 25.0
        self.bme680_sensor_mock.data.humidity = 50.0
        self.bme680_sensor_mock.data.pressure = 1013.0

    def test_get_data(self):
        sensor = Sensor()
        sensor.mhz19 = self.mh_z19_mock
        sensor.bme680 = self.bme680_sensor_mock
        data = sensor.get_data()
        self.assertEqual(data['temperature'], 25.0)
        self.assertEqual(data['humidity'], 50.0)
        self.assertEqual(data['pressure'], 1013.0)
        self.assertEqual(data['co2'], 400.0)

    def test_save_data(self):
        sensor = Sensor()
        sensor.mhz19 = self.mh_z19_mock
        sensor.bme680 = self.bme680_sensor_mock
        data = sensor.get_data()
        sensor.save_data(data)

        # Überprüfen, ob die Daten korrekt in der Datenbank gespeichert wurden
        self.assertEqual(IndoorSensorData.objects.count(), 1)
        saved_data = IndoorSensorData.objects.first()
        self.assertEqual(saved_data.temperature, 25.0)
        self.assertEqual(saved_data.humidity, 50.0)
        self.assertEqual(saved_data.pressure, 1013.0)
        self.assertEqual(saved_data.co2, 400.0)
