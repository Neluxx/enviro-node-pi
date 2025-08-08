from xml.dom import ValidationErr

from pi_sensor.models import IndoorSensorData


class SensorDataSaver:

    def save_data(self, data: dict[str, float]) -> None:
        try:
            IndoorSensorData(
                temperature=data["temperature"],
                humidity=data["humidity"],
                pressure=data["pressure"],
                co2=data["co2"],
            ).save()
        except ValidationErr:
            pass
