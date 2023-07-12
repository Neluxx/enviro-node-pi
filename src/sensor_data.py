#!/usr/bin/env python3
"""
Sensor Data
"""

import mh_z19
from db_conn import DatabaseConnection
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

    db_conn = DatabaseConnection()
    db_conn.insert_data(data)
    db_conn.close_connection()
