#!/usr/bin/env python3
"""
Sensor Data
"""

import mh_z19
from datetime import datetime


class SensorData:
    """Sensor Data Class"""

    def get_data(self):
        """Get data from sensor"""

        sensor_data = mh_z19.read_all()

        data = {
            "value": sensor_data["co2"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return data
