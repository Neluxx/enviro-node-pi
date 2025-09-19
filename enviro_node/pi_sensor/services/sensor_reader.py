from pi_sensor.sensors.sensor_factory import SensorFactory


class SensorReader:

    def __init__(self) -> None:
        self.co2_sensor = SensorFactory.create_mhz19_sensor()
        self.environmental_sensor = SensorFactory.create_bme680_sensor()

    def collect_data(self) -> dict[str, float]:
        environmental_data = self.environmental_sensor.get_data()
        co2_data = self.co2_sensor.get_data()

        return {**environmental_data, **co2_data}
