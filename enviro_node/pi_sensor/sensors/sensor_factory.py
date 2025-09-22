from enum import Enum
from typing import Protocol

from django.conf import settings


class SensorProtocol(Protocol):
    def get_data(self) -> dict[str, float]: ...


class SensorType(Enum):
    BME680 = "bme680"
    MHZ19 = "mhz19"


class SensorFactory:
    """Factory for creating sensor instances with better extensibility"""

    _sensor_registry = {
        SensorType.BME680: {
            "real": ("pi_sensor.sensors.bme680", "BME680Sensor"),
            "fake": ("pi_sensor.sensors.fake_bme680", "FakeBME680Sensor"),
        },
        SensorType.MHZ19: {
            "real": ("pi_sensor.sensors.mh_z19", "MHZ19Sensor"),
            "fake": ("pi_sensor.sensors.fake_mh_z19", "FakeMHZ19Sensor"),
        },
    }

    @classmethod
    def create_sensor(cls, sensor_type: SensorType) -> SensorProtocol:
        """Create a sensor instance based on type and settings"""
        if sensor_type not in cls._sensor_registry:
            raise ValueError(f"Unknown sensor type: {sensor_type}")

        sensor_config = cls._sensor_registry[sensor_type]
        variant = "fake" if settings.MOCK_SENSORS else "real"
        module_path, class_name = sensor_config[variant]

        module = __import__(module_path, fromlist=[class_name])
        sensor_class = getattr(module, class_name)

        return sensor_class()

    @classmethod
    def register_sensor(
        cls,
        sensor_type: SensorType,
        real_class: tuple[str, str],
        fake_class: tuple[str, str],
    ) -> None:
        """Register a new sensor type"""
        cls._sensor_registry[sensor_type] = {
            "real": real_class,
            "fake": fake_class,
        }
