try:
    import mh_z19  # type: ignore
except ImportError:
    mh_z19 = None


class MHZ19Sensor:

    def __init__(self) -> None:
        self.sensor = mh_z19.read_all()

    def get_data(self) -> dict:
        return {'co2': self.sensor['co2']}
