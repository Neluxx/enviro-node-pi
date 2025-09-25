import logging
import random

from .base_sensor import BaseSensor

logger = logging.getLogger(__name__)


class FakeBME680Sensor(BaseSensor):
    """Fake BME680 sensor for testing and development"""

    def __init__(self) -> None:
        logger.info("Fake BME680 sensor initialized")

    def get_data(self) -> dict[str, float]:
        """Generate realistic fake environmental data"""
        base_temp = 22.0
        base_humidity = 45.0
        base_pressure = 1013.25

        return {
            "temperature": round(base_temp + random.uniform(-2, 2), 2),
            "humidity": round(base_humidity + random.uniform(-5, 5), 2),
            "pressure": round(base_pressure + random.uniform(-10, 10), 2),
        }
