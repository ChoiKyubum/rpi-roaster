from menu import Menu
from roast import Roast
from time import sleep

process = "ready" # "ready" | "menu" | "roasting" 

_menu = Menu()

while True:
    if process == "ready":
        _menu.start()
        process = "menu"
    elif process == "menu" and _menu.is_done():
        process = "roasting"
    elif process == "roasting":
        Roast().start(_menu.get_menu())
        process = "ready"
    sleep(1)
    