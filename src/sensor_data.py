#!/usr/bin/env python3
"""
Sensor Data
"""

import board
import mh_z19
from busio import I2C
import adafruit_bme680
from datetime import datetime


class SensorData:
    """Sensor Data Class"""

    def __init__(self):
        self.temperature_offset = 0
        self.i2c = I2C(board.SCL, board.SDA)
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, debug=False)

    def get_data(self):
        """Get data from sensor"""

        sensor_data = mh_z19.read_all()

        data = {
            "value": sensor_data["co2"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return data

    def print_bme680_data(self):
        """Print data from BME680 sensor"""

        print(
            "Temperature: %0.1f C" % (self.bme680.temperature + self.temperature_offset)
        )
        print("Gas: %d ohm" % self.bme680.gas)
        print("Humidity: %0.1f %%" % self.bme680.relative_humidity)
        print("Pressure: %0.3f hPa" % self.bme680.pressure)
        print("Altitude = %0.2f meters" % self.bme680.altitude)
