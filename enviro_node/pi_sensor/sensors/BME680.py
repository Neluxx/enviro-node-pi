try:
    import bme680  # type: ignore
except ImportError:
    bme680 = None


class BME680Sensor:

    def __init__(self) -> None:
        self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        self._configure_sensor()

    def _configure_sensor(self) -> None:
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)

    def get_data(self) -> dict:
        return {
            'temperature': self.sensor.data.temperature,
            'humidity': self.sensor.data.humidity,
            'pressure': self.sensor.data.pressure,
        }

