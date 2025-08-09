import random


class FakeMHZ19Sensor:

    def get_data(self) -> dict[str, float]:
        return {"co2": random.uniform(400, 800)}
