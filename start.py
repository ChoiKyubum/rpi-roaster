from menu import Menu
from roast import Roast
from time import sleep
import asyncio

async def main():
    while True:
        _menu = Menu()
        _menu.start()
        selected_menu = await _menu.selected()
        Roast().start(selected_menu)
        sleep(1)

asyncio.run(main())