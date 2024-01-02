from apps.api.services import OpenWeather


class ApiDataCollector:
    def run(self):
        open_weather = OpenWeather()
        open_weather_data = open_weather.get_data()
        open_weather.save_data(open_weather_data)
