import logging
from typing import Dict

from pi_sensor.sensors.sensor_factory import SensorFactory, SensorProtocol, SensorType

logger = logging.getLogger(__name__)


class SensorReader:
    """Reads data from multiple sensors and combines results"""

    def __init__(self) -> None:
        self.sensors: Dict[SensorType, SensorProtocol] = {}
        self._initialize_sensors()

    def _initialize_sensors(self) -> None:
        """Initialize all requested sensors"""
        for sensor_type in SensorType:
            try:
                sensor = SensorFactory.create_sensor(sensor_type)
                self.sensors[sensor_type] = sensor
                logger.info(f"Initialized {sensor_type.value} sensor")
            except Exception as e:
                logger.error(f"Failed to initialize {sensor_type.value} sensor: {e}")

    def collect_data(self) -> dict[str, float]:
        """Collect data from all available sensors"""
        if not self.sensors:
            raise RuntimeError("No sensors available")

        combined_data = {}
        for sensor_type, sensor in self.sensors.items():
            try:
                sensor_data = sensor.get_data()
                combined_data.update(sensor_data)
                logger.debug(f"Read data from {sensor_type.value}: {sensor_data}")
            except Exception as e:
                logger.error(f"Failed to read data from {sensor_type.value}: {e}")

        return combined_data
