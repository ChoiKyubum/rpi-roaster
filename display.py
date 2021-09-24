import libs.RPi_I2C_driver as LCD_Driver
from time import sleep

class Display:
    def __init__(self):
        self.lcd = LCD_Driver.lcd(0x27)
        self.is_working = False

    def wait_working(self):
        while self.is_working:
            sleep(0.0001)
    
    def clear(self):
        self.wait_working()
        self.is_working = True
        self.lcd.clear()
        self.is_working = False
    
    def show(self, str, line):
        self.wait_working()
        self.is_working = True
        try:
            self.lcd.setCursor(0, line - 1)
            self.lcd.print(str.ljust(16, " "))
        except OSError as err:
            self.is_working = False
            print("LCD Error: {}".format(err))
            self.lcd = LCD_Driver.lcd(0x27)
            self.show(str, line)
        self.is_working = False