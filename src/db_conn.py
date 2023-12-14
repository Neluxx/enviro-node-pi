#!/usr/bin/env python3
"""
Database Connection
"""

import os
import mysql.connector
from datetime import datetime


class DatabaseConnection:
    """Database Connection Class"""

    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self):
        """Create database connection"""

        conn = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
        )

        if conn is None:
            print("Error connecting to database")
            raise ConnectionError

        return conn

    def insert_sensor_data(self, data):
        """Insert sensor data to database"""

        cursor = self.conn.cursor()
        sql = "INSERT INTO sensor_data (temperature, humidity, pressure, co2, created) VALUES (%s, %s, %s, %s, %s)"

        values = (
            data["temperature"],
            data["humidity"],
            data["pressure"],
            data["co2"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        cursor.execute(sql, values)
        self.conn.commit()

    def insert_open_weather_data(self, data):
        """Insert open weather data to database"""

        cursor = self.conn.cursor()
        sql = """INSERT INTO open_weather_data
        (temperature, feels_like, temp_min, temp_max, humidity, pressure, weather_main, weather_description, weather_icon, visibility, wind_speed, wind_deg, clouds, created)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (
            data["main"]["temp"],
            data["main"]["feels_like"],
            data["main"]["temp_min"],
            data["main"]["temp_max"],
            data["main"]["humidity"],
            data["main"]["pressure"],
            data["weather"][0]["main"],
            data["weather"][0]["description"],
            data["weather"][0]["icon"],
            data["visibility"],
            data["wind"]["speed"],
            data["wind"]["deg"],
            data["clouds"]["all"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        cursor.execute(sql, values)
        self.conn.commit()

    def close_connection(self):
        """Close database connection"""

        self.conn.close()
