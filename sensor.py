class Sensor:
    """Sensor Class"""

    MOCK_MHZ19_DATA = {"co2": 450}
    MOCK_BME680_DATA = {"temperature": 20, "humidity": 40, "pressure": 900}

    def __init__(self):
        self.mhz19 = self._initialize_mhz19()
        self.bme680 = self._initialize_bme680()

    def _initialize_mhz19(self):
        """Initialize MH-Z19 sensor."""
        try:
            import mh_z19
            return mh_z19.read_all()
        except ImportError:
            # Return mock data if MH-Z19 is unavailable
            return self.MOCK_MHZ19_DATA

    def _initialize_bme680(self):
        """Initialize BME680 sensor."""
        try:
            import bme680
            sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
            self._configure_bme680(sensor)
            return sensor
        except ImportError:
            # Return mock sensor if BME680 is unavailable
            return self._get_mock_bme680()

    def _configure_bme680(self, sensor):
        """Set oversampling and filter configurations for BME680."""
        sensor.set_humidity_oversample(sensor.OS_2X)
        sensor.set_pressure_oversample(sensor.OS_4X)
        sensor.set_temperature_oversample(sensor.OS_8X)
        sensor.set_filter(sensor.FILTER_SIZE_3)

    def _get_mock_bme680(self):
        """Create a mock BME680 sensor with predefined data."""
        class MockBME680:
            def __init__(self):
                self.data = type(
                    "MockData",
                    (object,),
                    Sensor.MOCK_BME680_DATA,
                )()
        return MockBME680()

    def get_data(self):
        """Get data from sensors."""
        return {
            "temperature": self.bme680.data.temperature,
            "humidity": self.bme680.data.humidity,
            "pressure": self.bme680.data.pressure,
            "co2": self.mhz19["co2"],
        }