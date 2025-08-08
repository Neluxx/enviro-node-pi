from pi_sensor.sensors.BME680 import BME680Sensor
from pi_sensor.sensors.MHZ19 import MHZ19Sensor


class SensorDataReader:

    def __init__(self) -> None:
        self.mhz19_sensor = MHZ19Sensor()
        self.bme680_sensor = BME680Sensor()

    def get_data(self) -> dict:
        bme_data = self.bme680_sensor.get_data()
        co2_data = self.mhz19_sensor.get_data()
        return {**bme_data, **co2_data}
