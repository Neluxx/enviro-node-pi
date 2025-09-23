from enum import Enum
from typing import Protocol, Type

from django.conf import settings

from pi_sensor.sensors.bme680 import BME680Sensor
from pi_sensor.sensors.fake_bme680 import FakeBME680Sensor
from pi_sensor.sensors.fake_mh_z19 import FakeMHZ19Sensor
from pi_sensor.sensors.mh_z19 import MHZ19Sensor


class SensorProtocol(Protocol):
    def get_data(self) -> dict[str, float]: ...


class SensorType(Enum):
    BME680 = "bme680"
    MHZ19 = "mhz19"


class SensorFactory:
    """Factory for creating sensor instances with better extensibility"""

    _sensor_registry: dict[SensorType, dict[str, Type[SensorProtocol]]] = {
        SensorType.BME680: {
            "real": BME680Sensor,
            "fake": FakeBME680Sensor,
        },
        SensorType.MHZ19: {
            "real": MHZ19Sensor,
            "fake": FakeMHZ19Sensor,
        },
    }

    @classmethod
    def create_sensor(cls, sensor_type: SensorType) -> SensorProtocol:
        """Create a sensor instance based on type and settings"""
        if sensor_type not in cls._sensor_registry:
            available_types = ", ".join(t.value for t in cls._sensor_registry.keys())
            raise ValueError(f"Unknown sensor type: {sensor_type.value}. Available types: {available_types}")

        sensor_classes = cls._sensor_registry[sensor_type]
        variant = "fake" if settings.MOCK_SENSORS else "real"
        sensor_class = sensor_classes[variant]

        return sensor_class()
