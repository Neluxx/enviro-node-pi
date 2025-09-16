from pi_sensor.sensors.sensor_factory import SensorFactory


class SensorReader:

    def __init__(self) -> None:
        self.mhz19_sensor = SensorFactory.create_mhz19_sensor()
        self.bme680_sensor = SensorFactory.create_bme680_sensor()

    def collect_data(self) -> dict[str, float]:
        bme_data = self.bme680_sensor.get_data()
        co2_data = self.mhz19_sensor.get_data()
        return {**bme_data, **co2_data}
