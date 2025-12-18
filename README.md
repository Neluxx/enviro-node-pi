# Enviro Node Pi

A Django-based environmental monitoring system for Raspberry Pi that collects sensor data and submits the data to a central EnviroHub API for analysis and visualization.

## Features

### Indoor Environmental Monitoring
- **[BME680](https://www.berrybase.ch/bme680-breakout-board-4in1-sensor-fuer-temperatur-luftfeuchtigkeit-luftdruck-und-luftguete) Sensor Integration**: Collects temperature, humidity, and air pressure measurements
- **[MH-Z19](https://www.berrybase.ch/mh-z19c-infrarot-co2-sensor-pinleiste) Sensor Integration**: Monitors CO2 concentration levels
- **Automated Data Collection**: Django management commands for scheduled sensor readings

### Data Submission & Synchronization
- **EnviroHub Client**: Automatic batch submission of sensor data to central API
- **Batch Processing**: Configurable batch sizes (default: 1000 records) for efficient data transfer
- **Submission Tracking**: Maintains submission status to prevent duplicate uploads
- **Error Handling**: Comprehensive logging with rotating file handlers

---

## Prerequisites

- Git
- Python 3.11+ (Installed in Pi OS Bookworm)
- Virtual environment (e.g. `virtualenv`)
- Raspberry Pi (Tested on Raspberry Pi 3B+)
  - BME680 Sensor (temperature, humidity, and air pressure)
  - MH-Z19 Sensor (CO2 concentration)

## Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/Neluxx/enviro-node-pi.git
   cd enviro-node-pi
   ```

2. **Setup virtual environment**
   ```bash
   python -m venv venv --system-site-packages
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # For development (includes testing tools):
   pip install -r requirements-dev.txt

   # For production:
   pip install -r requirements-prod.txt
   ```

4. **Configure environment variables**
   ```bash
   cd enviro_node
   cp .env.example .env

   nano .env # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

### Management Commands

#### Collect Sensor Data
   ```bash
python manage.py sensor_data_collector
   ```

#### Submit Sensor Data
```bash
python manage.py sensor_data_submitter
```

#### Reset Sensor Data
```bash
python manage.py sensor_data_resetter
```

---

## Development

### Running Test Suite
```bash
python manage.py test
```

### Code Coverage Report
```bash
coverage run manage.py test
coverage report # Generates report in terminal
coverage html # Generates HTML report in ./htmlcov/
```

### Code Quality Check
```bash
pre-commit install
pre-commit run --all-files
```

---

## Changelog

See [CHANGELOG](https://github.com/Neluxx/enviro-node-pi/blob/main/CHANGELOG.md) for version history and updates.

## Support

Please [open an issue](https://github.com/Neluxx/enviro-node-pi/issues/new) for support.

## License

See [LICENSE](https://github.com/Neluxx/enviro-node-pi/blob/main/LICENSE) for details.
