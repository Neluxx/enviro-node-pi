import logging
import random

from weather_station.sensors import BaseSensor

logger = logging.getLogger(__name__)


class FakeMHZ19Sensor(BaseSensor):
    """Fake MH-Z19 sensor for testing and development"""

    def __init__(self) -> None:
        logger.info("Fake MH-Z19 sensor initialized")

    def get_data(self) -> dict[str, float]:
        """Generate realistic fake CO2 data"""
        return {"co2": round(random.uniform(400, 800), 2)}
