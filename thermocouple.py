import board
import digitalio
import adafruit_max31865

class Thermo:
    def __init__(self):
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
        self.sensor = adafruit_max31865.MAX31865(spi, cs, wires=3)

    def get_temperature(self):
        return self.sensor.temperature
