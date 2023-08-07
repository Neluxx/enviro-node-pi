#!/usr/bin/env python3
"""
Sensor
"""

import mh_z19
import bme680


class Sensor:
    """Sensor Class"""

    def __init__(self):
        self.mhz19 = mh_z19.read_all()
        self.bme680 = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        self.bme680.set_humidity_oversample(bme680.OS_2X)
        self.bme680.set_pressure_oversample(bme680.OS_4X)
        self.bme680.set_temperature_oversample(bme680.OS_8X)
        self.bme680.set_filter(bme680.FILTER_SIZE_3)

    def get_data(self):
        """Get data from sensors"""

        data = {
            "temperature": self.bme680.data.temperature,
            "humidity": self.bme680.data.humidity,
            "pressure": self.bme680.data.pressure,
            "co2": self.mhz19["co2"],
        }

        return data
