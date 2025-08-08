import random


class FakeMHZ19Sensor:

    def get_data(self) -> dict:
        return {"co2": random.randint(400, 800)}
