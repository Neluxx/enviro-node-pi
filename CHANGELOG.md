# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Add a temperature offset by -3 degrees Celsius to the BME680 sensor [#9](https://github.com/Neluxx/enviro-node-pi/issues/9)

### Changed

### Deprecated

### Removed

### Fixed

### Security

### Dependencies

## [v1.1.1](https://github.com/Neluxx/enviro-node-pi/releases/tag/v1.1.1) - 2025-10-28

### Security
- Remove the logging of sensitive information [#3](https://github.com/Neluxx/enviro-node-pi/security/code-scanning/3)

## [v1.1.0](https://github.com/Neluxx/enviro-node-pi/releases/tag/v1.1.0) - 2025-10-28

### Changed
- Make MH-Z19 CO2 value optional and disable validation when missing [#3](https://github.com/Neluxx/enviro-node-pi/issues/3)

### Dependencies
- Update bme680 from 1.1.1 to 2.0.0 major [#5](https://github.com/Neluxx/enviro-node-pi/issues/5)

## [v1.0.0](https://github.com/Neluxx/enviro-node-pi/releases/tag/v1.0.0) - 2025-10-24

### Added

- Sensor Integration
  - Add support for BME680 sensor to collect temperature, humidity, and pressure data
  - Add support for MH-Z19 sensor to collect CO2 concentration data
  - Add fake sensor implementations for testing and development without hardware

- Sensor Data Management
  - Add automatic sensor data collection via management command
  - Add automatic submission of sensor data to EnviroHub API in batches
  - Add sensor factory with dynamic module loading for flexible sensor management

- OpenWeather Integration
  - Add OpenWeather API integration to retrieve current weather data
  - Add automatic weather data collection and storage via management command
  - Add automatic submission of weather data to EnviroHub API in batches

- Logging
  - Add rotating file handler for error logging with size limits
