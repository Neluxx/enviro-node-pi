import logging
from typing import Optional

import bme680  # type: ignore

from .base_sensor import BaseSensor

logger = logging.getLogger(__name__)


class BME680Sensor(BaseSensor):
    """BME680 Environmental Sensor"""

    def __init__(self, i2c_addr: Optional[int] = None) -> None:
        self.sensor: Optional[bme680.BME680] = None
        self.i2c_addr = i2c_addr or bme680.I2C_ADDR_SECONDARY
        self._initialize_sensor()

    def _initialize_sensor(self) -> None:
        """Initialize and configure the BME680 sensor"""
        try:
            self.sensor = bme680.BME680(self.i2c_addr)
            self._configure_sensor()

            logger.info("BME680 sensor initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize BME680 sensor: {e}")
            raise RuntimeError(f"BME680 sensor initialization failed: {e}") from e

    def _configure_sensor(self) -> None:
        """Configure sensor settings for optimal performance"""
        if not self.sensor:
            return

        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)

    def get_data(self) -> dict[str, float]:
        """Get temperature, humidity, and pressure data"""
        if not self.sensor:
            raise RuntimeError("Sensor not initialized")

        try:
            if self.sensor.get_sensor_data():
                return {
                    "temperature": round(self.sensor.data.temperature, 2),
                    "humidity": round(self.sensor.data.humidity, 2),
                    "pressure": round(self.sensor.data.pressure, 2),
                }
            else:
                raise RuntimeError("Failed to read sensor data")

        except Exception as e:
            logger.error(f"Error reading BME680 data: {e}")
            raise RuntimeError(f"Failed to read BME680 data: {e}") from e
