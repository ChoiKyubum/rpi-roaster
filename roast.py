from thermocouple import Thermo
from gpiozero import LED
from time import sleep
from buttons import setup_button_callback
from display import Display
import math
from datetime import datetime 

fan = LED(17)
heater = LED(27)
period = 0.25

ROASTING = "ROASTING"
COOLING = "COOLING"

class Roast:
    def __init__(self):
        self.target_temperature = 195
        self.target_ror = 1.8
        self.rors = []
        self.heater_on = True
        self.working = True
        self.current_temperature = None
        self.thermo = None
        self.display = Display()
        self.start_time = 0
        self.end_time = 0
        self.process = ROASTING

    def start(self, menu):
        self.display.clear()
        self.display.show("Start Roasting!", 1)
        sleep(1)
        fan.on()
        sleep(0.5)
        heater.on()
        self.start_time = datetime.now()
        self.thermo = Thermo()
        self.current_temperature = self.thermo.get_temperature()
        if menu == "Custom":
            setup_button_callback(self.custom_control_callbacks)

        while self.roast(menu):
            sleep(period)
        fan.off()
        sleep(5)
    
    def roast(self, menu):
        temp = self.thermo.get_temperature()
        if self.heater_on == True:
            self.set_heater(temp)
        elif heater.value == 1:
            heater.off()
        self.display_status(temp)
        self.current_temperature = temp
        return self.is_done()

    def is_done(self):
        if self.process == COOLING:
            return self.current_temperature < 60
        return True
            
    def set_heater(self, temp):
        if self.target_temperature <= temp:
            if heater.value == 1:
                heater.off()
            return

        if self.get_ror(temp) > self.target_ror:
            heater.off()
            return
            
        heater.on()

    def get_ror(self, temp):
        current_ror = (temp - self.current_temperature) / period
        self.rors.append(current_ror)
        if len(self.rors) > 10:
            self.rors.pop(0)
        return sum(self.rors) / len(self.rors)

    def custom_control_callbacks(self, action):
        if action == "left":
            self.target_temperature -= 10
            self.display_status(self.thermo.get_temperature())
        if action == "right":
            self.target_temperature += 10
            self.display_status(self.thermo.get_temperature())
        if action == "confirm":
            self.heater_on = False
            self.display.show("Start Cooling", 1)
            self.end_time = datetime.now()
            self.process = COOLING

    def display_status(self, temp):
        if self.process == COOLING:
            avg_ror = sum(self.rors) / len(self.rors)
            status = "{}|{:0.3f}|{:0.3f}".format(self.target_temperature, temp, avg_ror)
            self.display.show(status, 1)
            self.display.show(self.get_time_text(datetime.now()), 2)
        else:
            self.display.show("Cooling", 1)
            self.display.show(self.get_time_text(self.end_time), 2)

    def get_time_text(self, time):
        duration_seconds = (time - self.start_time).seconds
        minutes = "{}".format(math.floor(duration_seconds / 60)).rjust(2, "0")
        seconds = "{}".format(duration_seconds % 60).rjust(2, "0")
        return "{}:{}".format(minutes, seconds)