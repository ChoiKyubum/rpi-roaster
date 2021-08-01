from time import sleep
from display import Display
from buttons import setup_button_callback

menu = ["Light", "Medium", "Dark", "Custom"]

class Menu:
    def __init__(self):
        self.done = False
        self.current_menu_index = 0
        self.display = Display()


    def start(self):
        self.done = False
        self.display.clear()
        self.display.show("RPi Roaster !", 1)
        self.display.show("Press any button", 2)

        setup_button_callback(lambda _: self.display_menus())

    def display_menus(self):
        self.display.clear()
        self.display.show("Select Roasting", 1)
        self.display_menu()
        setup_button_callback(self.button_callback)

    def display_menu(self):
        self.display.show(menu[self.current_menu_index], 2)

    def button_callback(self, action):
        if self.done == True:
            return
        if action == "left":
            self.current_menu_index = (self.current_menu_index - 1) % len(menu)
            self.display_menu()
        if action == "right":
            self.current_menu_index = (self.current_menu_index + 1) % len(menu)
            self.display_menu()
        if action == "confirm":
            self.done = True
            self.display.clear()
            self.display.show("Menu Selected!", 1)
            self.display.show("\"{}\"".format(menu[self.current_menu_index]), 2)
            sleep(1)

    def get_menu(self):
        return menu[self.current_menu_index]
    
    def is_done(self):
        return self.done
