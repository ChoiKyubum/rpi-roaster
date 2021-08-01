from gpiozero import Button

left_button = Button(24)
confirm_button = Button(23)
right_button = Button(22)

def setup_button_callback(callback):
    left_button.when_pressed = lambda : callback("left")
    confirm_button.when_pressed = lambda : callback("confirm")
    right_button.when_pressed = lambda : callback("right")