#!/usr/bin/env python3
"""
Raspberry Pi Sensor Data
"""

__author__ = "Fabian Arndt"
__version__ = "0.1.0"
__license__ = "MIT"


import mh_z19
import database
from datetime import datetime


def run():
    """Main method"""

    get_sensor_data()


def get_sensor_data():
    """Get data from sensor"""

    data = mh_z19.read_all()
    save_sensor_data(data)


def save_sensor_data(data):
    """Save sensor data into database"""

    data = {
        "value": data["co2"],
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    database.insert_sensor_data(data)


if __name__ == "__main__":
    run()
