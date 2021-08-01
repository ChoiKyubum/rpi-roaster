import libs.RPi_I2C_driver as LCD_Driver
from time import sleep

class Display:
    def __init__(self):
        self.lcd = LCD_Driver.lcd(0x27)
    
    def clear(self):
        self.lcd.clear()
    
    def show(self, str, line):
        try:
            self.lcd.setCursor(0, line - 1)
            self.lcd.print(str.ljust(16, " "))
        except OSError as err:
            print(err)
            self.lcd = LCD_Driver.lcd(0x27)
            self.show(str, line)