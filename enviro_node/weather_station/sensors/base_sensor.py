from abc import ABC, abstractmethod


class BaseSensor(ABC):
    """Base sensor class with common functionality"""

    @abstractmethod
    def get_data(self) -> dict[str, float]:
        """Get sensor data"""
        pass
