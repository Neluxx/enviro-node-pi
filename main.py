#!/usr/bin/env python3
"""
Raspberry Pi Sensor Data
"""

__author__ = "Fabian Arndt"
__version__ = "0.1.0"
__license__ = "MIT"


import mh_z19


def get_sensor_data() -> None:
    """Get data from sensor"""
    data = mh_z19.read_all()
    save_sensor_data(data)


def save_sensor_data(data) -> None:
    """Save sensor data into database"""
    co2 = data["co2"]
    temperature = data["temperature"]
    print("CO2: ", co2)
    print("Temperature: ", temperature)


if __name__ == "__main__":
    get_sensor_data()
