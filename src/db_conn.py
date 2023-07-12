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

        sql = "INSERT INTO co2 (value, created) VALUES (%s, %s)"
        values = (data["value"], data["created"])
        cursor.execute(sql, values)

        self.conn.commit()

    def close_connection(self):
        """Close database connection"""

        self.conn.close()
