# Raspberry PI Weather Station

The project consists of realising a small weather station with a Raspberry Pi.

Two sensors were used to take indoor measurements. One is the [BME680](https://www.berrybase.ch/bme680-breakout-board-4in1-sensor-fuer-temperatur-luftfeuchtigkeit-luftdruck-und-luftguete), which measures the temperature, humidity and air pressure, and the other is the [MH-Z19](https://www.berrybase.ch/mh-z19c-infrarot-co2-sensor-pinleiste), which measures the CO2 concentration in the air.

There is also an API to [OpenWeatherMap](https://openweathermap.org/), which can be used to collect weather data for a defined specified outdoor location.

A command can be used to record the sensor data, which is then saved in a database. If the CO2 limit value is exceeded, an e-mail is automatically sent via [ElasticEmail](https://elasticemail.com/) with a request for ventilation.

There is also a command that calls the OpenWeatherMap API and saves the result in the database.

In future, it should be possible to create diagrams from the data collected in the database. These should visualise indoor and outdoor weather data and thus allow conclusions to be drawn about air quality or similar.

## Prerequisites

- Install [Git](https://git-scm.com/downloads)
- Install [Python](https://www.python.org/downloads/)

## Installation

- Clone the repository `git clone https://github.com/Neluxx/raspberrypi-weather-station.git`
- Go into the project directory `cd raspberrypi-weather-station`
- Setup the project `pip install -r requirements.txt`

## Usage

- Go into the django project directory `cd raspberrypi-weather-station/enviro_node`
- Run the project `python manage.py runserver`
- Visit [Localhost](http://127.0.0.1:8000/)

## Support

Please [open an issue](https://github.com/Neluxx/raspberrypi-weather-station/issues/new) for support.
