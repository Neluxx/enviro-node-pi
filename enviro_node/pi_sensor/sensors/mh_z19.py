import logging
from typing import Optional

import mh_z19  # type: ignore

from .base_sensor import BaseSensor

logger = logging.getLogger(__name__)


class MHZ19Sensor(BaseSensor):
    """MH-Z19 CO2 Sensor"""

    def __init__(self, serial_device: Optional[str] = None) -> None:
        self.serial_device = serial_device
        self._test_connection()

    def _test_connection(self) -> None:
        """Test sensor connection during initialization"""
        try:
            test_data = mh_z19.read_all(serial_device_path=self.serial_device)

            if test_data is None or "co2" not in test_data:
                raise RuntimeError("No valid data received from MH-Z19 sensor")

            logger.info("MH-Z19 sensor connection verified")

        except Exception as e:
            logger.error(f"Failed to connect to MH-Z19 sensor: {e}")
            raise RuntimeError(f"MH-Z19 sensor connection failed: {e}") from e

    def get_data(self) -> dict[str, float]:
        """Get CO2 concentration data"""
        try:
            sensor_data = mh_z19.read_all(serial_device_path=self.serial_device)

            if sensor_data is None or "co2" not in sensor_data:
                raise RuntimeError("Invalid sensor data received")

            co2_value = sensor_data.get("co2")
            if co2_value is None or co2_value < 0:
                raise RuntimeError(f"Invalid CO2 reading: {co2_value}")

            return {"co2": float(co2_value)}

        except Exception as e:
            logger.error(f"Error reading MH-Z19 data: {e}")
            raise RuntimeError(f"Failed to read MH-Z19 data: {e}") from e
