try:
    import mh_z19  # type: ignore
    import bme680  # type: ignore
except ImportError:
    # Mock-Module oder Dummy-Module können hier zugewiesen werden, wenn sie für Tests benötigt werden.
    mh_z19 = None
    bme680 = None

from .models import IndoorSensorData


class Sensor:
    """Sensor Class"""

    def __init__(self) -> None:
        self.mhz19 = mh_z19.read_all()
        self.bme680 = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        self.bme680.set_humidity_oversample(bme680.OS_2X)
        self.bme680.set_pressure_oversample(bme680.OS_4X)
        self.bme680.set_temperature_oversample(bme680.OS_8X)
        self.bme680.set_filter(bme680.FILTER_SIZE_3)

    def get_data(self) -> dict:
        """Get data from sensors"""

        data: dict = {
            'temperature': self.bme680.data.temperature,
            'humidity': self.bme680.data.humidity,
            'pressure': self.bme680.data.pressure,
            'co2': self.mhz19['co2'],
        }

        return data

    def save_data(self, data: dict) -> None:
        IndoorSensorData(
            temperature=data['temperature'],
            humidity=data['humidity'],
            pressure=data['pressure'],
            co2=data['co2'],
        ).save()
