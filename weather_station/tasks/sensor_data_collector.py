from weather_station.apps.sensor.services import Sensor


class SensorDataCollector:
    def run(self):
        sensor = Sensor()
        sensor_data = sensor.get_data()
        sensor.save_data(sensor_data)
