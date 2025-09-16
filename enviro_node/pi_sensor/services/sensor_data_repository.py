from xml.dom import ValidationErr

from pi_sensor.models import IndoorSensorData


class SensorDataRepository:

    def insert(self, data: dict[str, float]) -> None:
        try:
            IndoorSensorData(
                temperature=data["temperature"],
                humidity=data["humidity"],
                pressure=data["pressure"],
                co2=data["co2"],
            ).save()
        except KeyError:
            pass
        except ValidationErr:
            pass
