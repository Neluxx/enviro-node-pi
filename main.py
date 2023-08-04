#!/usr/bin/env python3
"""
Raspberry Pi Sensor Data
"""

__author__ = "Fabian Arndt"
__version__ = "0.1.0"
__license__ = "MIT"


from dotenv import load_dotenv
from src.sensor import Sensor
from src.open_weather import OpenWeather
from src.db_conn import DatabaseConnection


def run():
    """Main Method"""

    load_dotenv()

    open_weather = OpenWeather()
    open_weather_data = open_weather.get_data()

    db_conn = DatabaseConnection('open_weather_data')
    db_conn.insert_open_weather_data(open_weather_data)
    db_conn.close_connection()

    sensor = Sensor()
    sensor_data = sensor.get_data()

    db_conn = DatabaseConnection('sensor_data')
    db_conn.insert_sensor_data(sensor_data)
    db_conn.close_connection()


if __name__ == "__main__":
    run()
