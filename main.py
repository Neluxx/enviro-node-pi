#!/usr/bin/env python3
"""
Raspberry Pi Sensor Data
"""

__author__ = "Fabian Arndt"
__version__ = "0.1.0"
__license__ = "MIT"


from dotenv import load_dotenv
from src.sensor_data import SensorData
from src.db_conn import DatabaseConnection


def run():
    """Main Method"""

    load_dotenv()
    sensor_data = SensorData()
    data = sensor_data.get_data()

    db_conn = DatabaseConnection()
    db_conn.insert_data(data)

    db_conn.close_connection()


if __name__ == "__main__":
    run()
