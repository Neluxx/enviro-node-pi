#!/usr/bin/env python3
"""
Database
"""

import os
import mysql.connector
from dotenv import load_dotenv


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
        load_dotenv()
        return mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
        )
    except ConnectionError:
        print("Error connecting to database")
