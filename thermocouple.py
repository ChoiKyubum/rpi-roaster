import board
import digitalio
import adafruit_max31855

class Thermo:
    def __init__(self):
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D5)
        self.sensor = adafruit_max31855.MAX31855(spi, cs)
        self.temperature = self.sensor.temperature

    def get_temperature(self):
        try:
            self.temperature = self.sensor.temperature
        except RuntimeError as err:
            print("Max31855: {}".format(err))
        return self.temperature

