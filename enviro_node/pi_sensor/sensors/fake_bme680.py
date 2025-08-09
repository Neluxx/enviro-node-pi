import random


class FakeBME680Sensor:

    def get_data(self) -> dict[str, float]:
        base_temp = 22.0
        base_humidity = 45.0
        base_pressure = 1013.25

        return {
            "temperature": round(base_temp + random.uniform(-2, 2), 2),
            "humidity": round(base_humidity + random.uniform(-5, 5), 2),
            "pressure": round(base_pressure + random.uniform(-10, 10), 2),
        }
