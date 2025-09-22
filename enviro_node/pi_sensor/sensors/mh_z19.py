import logging

import mh_z19  # type: ignore

from .base_sensor import BaseSensor

logger = logging.getLogger(__name__)


class MHZ19Sensor(BaseSensor):
    """MH-Z19 CO2 Sensor"""

    def get_data(self) -> dict[str, float]:
        """Get CO2 concentration data"""
        try:
            sensor_data = mh_z19.read_all()

            if sensor_data is None or "co2" not in sensor_data:
                raise RuntimeError("Invalid sensor data received")

            co2_value = sensor_data.get("co2")
            if co2_value is None or co2_value < 0:
                raise RuntimeError(f"Invalid CO2 reading: {co2_value}")

            return {"co2": float(co2_value)}

        except Exception as e:
            logger.error(f"Error reading MH-Z19 data: {e}")
            raise RuntimeError(f"Failed to read MH-Z19 data: {e}") from e
