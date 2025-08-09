from typing import Protocol

from django.conf import settings


class SensorProtocol(Protocol):
    def get_data(self) -> dict[str, float]: ...


class SensorFactory:
    @staticmethod
    def create_bme680_sensor() -> SensorProtocol:
        if settings.MOCK_SENSORS:
            from pi_sensor.sensors.FakeBME680 import FakeBME680Sensor

            return FakeBME680Sensor()
        else:
            from pi_sensor.sensors.BME680 import BME680Sensor

            return BME680Sensor()

    @staticmethod
    def create_mhz19_sensor() -> SensorProtocol:
        if settings.MOCK_SENSORS:
            from pi_sensor.sensors.FakeMHZ19 import FakeMHZ19Sensor

            return FakeMHZ19Sensor()
        else:
            from pi_sensor.sensors.MHZ19 import MHZ19Sensor

            return MHZ19Sensor()
