"""
File where the drivers for different power sources are parsed into a format that works universally with software to run them as expected, so the bulk code does not need to be changed based on which motors are being used.
"""

from abc import ABC, abstractmethod

class Driver(ABC):
    # Class that defines the different driver functions and properties,
    # inherited by Driver classes which can define each function as desired.
    def __init__(self, bitrate, port: str):
        self.bitrate = bitrate
        self.port = port
        self.device = self._init_device()
        self.calibrate()

    @abstractmethod
    def _init_device(self):
        # Initialise a controller with
        pass

    @abstractmethod
    def calibrate(self):
        # Calibration function for a given controller
        pass