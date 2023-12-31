import mh_z19
import bme680

from django.utils import timezone

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
            "temperature": self.bme680.data.temperature,
            "humidity": self.bme680.data.humidity,
            "pressure": self.bme680.data.pressure,
            "co2": self.mhz19["co2"],
        }

        return data

    def save_data(self, data: dict) -> None:
        IndoorSensorData(
            temperature=data["temperature"],
            humidity=data["humidity"],
            pressure=data["pressure"],
            co2=data["co2"],
            created=timezone.now(),
        ).save()

    def debug_mhz19(self) -> None:
        mhz19 = mh_z19.read_all()

        print("MH-Z19")
        print("CO2:", mhz19["co2"])

    def debug_bme680(self) -> None:
        try:
            sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        # These oversampling settings can be tweaked to change
        # the balance between accuracy and noise in the data.
        sensor.set_humidity_oversample(bme680.OS_2X)
        sensor.set_pressure_oversample(bme680.OS_4X)
        sensor.set_temperature_oversample(bme680.OS_8X)
        sensor.set_filter(bme680.FILTER_SIZE_3)

        if sensor.get_sensor_data():
            output = "{0:.2f} C,{1:.2f} hPa,{2:.3f} %RH".format(
                sensor.data.temperature, sensor.data.pressure, sensor.data.humidity
            )
            print(output)
