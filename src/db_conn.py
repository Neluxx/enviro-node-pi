#!/usr/bin/env python3
"""
Database Connection
"""

import os
import mysql.connector


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

    def insert_data(self, data):
        """Insert data to database"""

        cursor = self.conn.cursor()

        sql = "INSERT INTO sensor_data (temperature, relative_humidity, humidity, pressure, altitude, gas, co2, created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        values = (
            data["temperature"],
            data["relative_humidity"],
            data["humidity"],
            data["pressure"],
            data["altitude"],
            data["gas"],
            data["co2"],
            data["created"],
        )

        cursor.execute(sql, values)

        self.conn.commit()

    def close_connection(self):
        """Close database connection"""

        self.conn.close()
