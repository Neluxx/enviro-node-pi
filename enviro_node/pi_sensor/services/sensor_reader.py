import logging
from typing import Dict, List, Optional

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
        successful_reads = 0

        for sensor_type, sensor in self.sensors.items():
            try:
                sensor_data = sensor.get_data()
                combined_data.update(sensor_data)
                successful_reads += 1
                logger.debug(
                    f"Successfully read data from {sensor_type.value}: {sensor_data}"
                )
            except Exception as e:
                logger.error(f"Failed to read data from {sensor_type.value}: {e}")

        if successful_reads == 0:
            raise RuntimeError("Failed to read data from any sensor")

        logger.info(
            f"Collected data from {successful_reads}/{len(self.sensors)} sensors"
        )
        return combined_data

    def get_available_sensors(self) -> List[SensorType]:
        """Get list of successfully initialized sensors"""
        return list(self.sensors.keys())
