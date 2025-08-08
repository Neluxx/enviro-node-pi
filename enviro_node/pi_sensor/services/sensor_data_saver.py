from xml.dom import ValidationErr

from pi_sensor.models import IndoorSensorData


class SensorDataSaver:

    def save_data(self, data: dict) -> None:
        try:
            IndoorSensorData(
                temperature=data["temperature"],
                humidity=data["humidity"],
                pressure=data["pressure"],
                co2=data["co2"],
            ).save()
        except ValidationErr as e:
            # logger.error(f"Validation failed: {e}")
            pass
