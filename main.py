#!/usr/bin/env python3
"""
Raspberry Pi Sensor Data
"""

__author__ = "Fabian Arndt"
__version__ = "0.1.0"
__license__ = "MIT"


from dotenv import load_dotenv
from src.sensor_data import get_sensor_data


def main():
    """Main Method"""

    load_dotenv()
    get_sensor_data()


if __name__ == "__main__":
    main()
