from thermocouple import Thermo
from gpiozero import LED
from time import sleep
from buttons import setup_button_callback
from display import Display
import math

fan = LED(17)
heater = LED(27)

class Roast:
    def __init__(self):
        self.target_temperature = 190
        self.target_ror = 0.5
        self.seconds = 0
        self.heater_on = True
        self.working = True
        self.current_temperature = None
        self.thermo = None
        self.display = Display()

    def start(self, menu):
        self.display.clear()
        self.display.show("Start Roasting!", 1)
        sleep(1)
        fan.on()
        sleep(0.5)
        heater.on()
        self.thermo = Thermo()
        self.current_temperature = self.thermo.get_temperature()
        if menu == "Custom":
            setup_button_callback(self.custom_control_callbacks)

        while self.roast(menu):
            sleep(1)
            self.seconds += 1
        fan.off()
        sleep(5)
    
    def roast(self, menu):
        temp = self.thermo.get_temperature()
        self.display_status(temp)
        if self.heater_on == True:
            self.set_heater(temp)
        elif heater.value == 1:
            heater.off()
        self.current_temperature = temp
        return self.working
            
    def set_heater(self, temp):
        if self.target_temperature <= temp and heater.value == 1:
            heater.off()
            return

        if self.get_ror(temp) > self.target_ror:
            heater.off()
            return
            
        heater.on()

    def get_ror(self, temp):
        return temp - self.current_temperature

    def custom_control_callbacks(self, action):
        if action == "left":
            self.target_temperature -= 10
            self.display_status(self.thermo.get_temperature())
        if action == "right":
            self.target_temperature += 10
            self.display_status(self.thermo.get_temperature())
        if action == "confirm":
            if self.heater_on:
                self.heater_on = False
                self.display.show("Heater OFF", 1)
            else :
                self.display.show("Finish Roasting", 1)
                self.working = False

    def display_status(self, temp):
        status = "{}|{:0.3f}|{:0.3f}".format(self.target_temperature, temp, self.get_ror(temp))
        minutes = "{}".format(math.floor(self.seconds / 60)).rjust(2, "0")
        seconds = "{}".format(self.seconds % 60).rjust(2, "0")
        time = "{}:{}".format(minutes, seconds)
        self.display.show(status, 1)
        self.display.show(time, 2)
