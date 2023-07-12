#!/usr/bin/env python3
"""
Raspberry Pi Sensor Data
"""

__author__ = "Fabian Arndt"
__version__ = "0.1.0"
__license__ = "MIT"


import os
import mh_z19
import mariadb
from datetime import datetime


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

    insert_sensor_data(data)


def insert_sensor_data(data):
    """Insert sensor data to database"""

    conn = create_database_connection()

    cursor = conn.cursor()

    sql = "INSERT INTO co2 (value, created) VALUES (%s, %s)"
    val = (data["value"], data["created"])
    cursor.execute(sql, val)

    conn.commit()
    conn.close()


def create_database_connection():
    """Create database connection"""

    try:
        return mariadb.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
        )
    except mariadb.Error as exception:
        print(f"Error connecting to MariaDB Platform: {exception}")


if __name__ == "__main__":
    get_sensor_data()
