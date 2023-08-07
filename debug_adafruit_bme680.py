#!/usr/bin/env python3
"""
Adafruit BME680
"""

import adafruit_bme680
import board


def run():
    """Main Method"""

    # Create sensor object, communicating over the board's default I2C bus
    i2c = board.I2C()   # uses board.SCL and board.SDA
    ada_bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

    # change this to match the location's pressure (hPa) at sea level
    ada_bme680.sea_level_pressure = 1013.25

    print("Adafruit BME680")
    print("\nTemperature: %0.1f C" % ada_bme680.temperature)
    print("Gas: %d ohm" % ada_bme680.gas)
    print("Humidity: %0.1f %%" % ada_bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % ada_bme680.pressure)
    print("Altitude = %0.2f meters" % ada_bme680.altitude)


if __name__ == "__main__":
    run()
