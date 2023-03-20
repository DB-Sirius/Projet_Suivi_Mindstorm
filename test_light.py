#!/usr/bin/env python3

import os      # to set font
import time    # to use sleep()
import socket  # to get host name
from ev3dev2.sound   import Sound
from ev3dev2.display import Display
from ev3dev2.button  import Button
from ev3dev2.led     import Leds
from ev3dev2.motor   import MoveSteering, MediumMotor
from ev3dev2.motor   import OUTPUT_A, OUTPUT_D
from ev3dev2.sensor.lego import UltrasonicSensor, ColorSensor
from ev3dev2.sensor.lego import GyroSensor, TouchSensor
from PIL             import Image  # should not be needed, but IT IS!

# === Various functions to simplify calls ============================
def clear_display(display):
    display.clear()
    display.update()


def print_display(display, text):
    # using display.text_grid(text, ...) instead of print(test)
    display.text_grid(text, True, 0, 10)  # clear screen, 11th row / 22
    display.update()


def show_image(display, name):
    """ Print on the display the image of given name. """
    display.image.paste(Image.open('/home/robot/images/' + name + '.bmp'),
                        (0, 0))
    display.update()


def set_colors(leds, left_color, right_color):
    """ Change the leds colors to those given. """
    leds.set_color('LEFT', left_color)
    leds.set_color('RIGHT', right_color)


def wait_for_any_release(button):
    """ Wait for any button to be released. """
    button.wait_for_released(['backspace', 'up', 'down',
                              'left', 'right', 'enter'])

def intro(noisy, sound, display, tune = False):
    """ Checking sound (song & text to speach convertor)
    and display (clear & . """
    show_image(display, 'EV3')
    if (noisy):
        host_letter = socket.gethostname()[4]
        sound.speak('Hello, I am E V 3 ' + host_letter + '!')
    show_image(display, 'Neutral')
    return sound

def main(noisy = True):
    """Select which test to start using the box buttons."""
    sound   = Sound()
    display = Display()
    looping = True
    button  = Button()
    leds    = Leds()

    os.system('setfont Lat15-TerminusBold14')
    intro(noisy, sound, display)
    while (looping):
            # Avoid taking twice the same action
            wait_for_any_release(button) 

# When this module is called, it starts the main function.
if __name__ == "__main__":
    main()
