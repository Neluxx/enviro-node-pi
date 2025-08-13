from xml.dom import ValidationErr

from open_weather.models import OutdoorWeatherData


class OpenWeatherDataSaver:

    def save_data(self, data: dict) -> None:
        try:
            OutdoorWeatherData(
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                temp_min=data["main"]["temp_min"],
                temp_max=data["main"]["temp_max"],
                humidity=data["main"]["humidity"],
                pressure=data["main"]["pressure"],
                weather_main=data["weather"][0]["main"],
                weather_description=data["weather"][0]["description"],
                weather_icon=data["weather"][0]["icon"],
                visibility=data["visibility"],
                wind_speed=data["wind"]["speed"],
                wind_deg=data["wind"]["deg"],
                clouds=data["clouds"]["all"],
            ).save()
        except KeyError:
            pass
        except ValidationErr:
            pass
