#!/usr/bin/env python3

import os      # to set font
import time    # to use sleep()
import socket  # to get host name
from ev3dev2.display import Display
from ev3dev2.button  import Button
from ev3dev2.led     import Leds
from ev3dev2.motor   import MoveSteering, MediumMotor
from ev3dev2.motor   import OUTPUT_A, OUTPUT_D
from ev3dev2.sensor.lego import UltrasonicSensor, ColorSensor
from ev3dev2.sensor.lego import GyroSensor, TouchSensor
from ev3dev2.motor import OUTPUT_B, MoveTank, SpeedPercent, follow_for_ms
from PIL             import Image  # Je sais pas ce que ca fait mais laissons le


def print_display(display, text):
    # using display.text_grid(text, ...) instead of print(test)
    display.text_grid(text, True, 0, 10) # clear screen, 11th row / 22
    display.update()



def main(noisy = True):
    display = Display()
    us_sensor = UltrasonicSensor()
    steer_motors = MoveSteering(OUTPUT_A, OUTPUT_D)

    os.system('setfont Lat15-TerminusBold14')

    print_display(display,  'Debut')
    
    steer_motors.on(-100, 15)
    sleep(5)

    print_display(display,  'fin')
    sleep(5)





# When this module is called, it starts the main function.
if __name__ == "__main__":
    main()