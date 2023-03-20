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
from PIL             import Image  # Je sais pas ce que ca fait mais laissons le

def clear_display(display):
    display.clear()
    display.update()

def print_display(display, text):
    # using display.text_grid(text, ...) instead of print(test)
    display.text_grid(text, True, 0, 10) # clear screen, 11th row / 22
    display.update()

def tournerDroite(angle, gyro, steer_motors):
    values_gyro_init = gyro.angle_and_rate
    values_gyro_actual = gyro.angle_and_rate
    while(values_gyro_actual[0] < values_gyro_init[0] + angle): #tant qu'on est pas à l'angle de décalage demandé
        steer_motors.on(-100, 5)
        time.sleep(0.5)
        steer_motors.off()
        values_gyro_actual = gyro.angle_and_rate

    



def main(noisy = True):
    display = Display()
    us_sensor = UltrasonicSensor()
    steer_motors = MoveSteering(OUTPUT_A, OUTPUT_D)
    gyro_sensor = GyroSensor()
    os.system('setfont Lat15-TerminusBold14')
    
    #Valeur du pas (en degrés)
    step = 10 #N'UTILISER QUE DES DIVISEURS DE 360!!!!
    if(False): #se démerder pour avoir une condidiopn qui marche
        print_display(display,  'Pas invalide')
        time.sleep(2)
        exit()
    nbCases = 360/step #convertir en entier

    nbPas = 36

    print_display(display,  'CALIBRATION')
    gyro_sensor.calibrate()
    time.sleep(1)

    tabloDistance = []
    print_display(display,  'Début scan')
    time.sleep(2)
    #Boucle principale de scan
    for i in range(nbPas): 
        dist = us_sensor.distance_centimeters
        print_display(display,  'Distance: ' + str(dist) )
        tabloDistance.append(dist)
        tournerDroite(10, gyro_sensor, steer_motors)
        time.sleep(0.5)

    #On dump le tableau des distances dans un txt pour pouvoir les rapatrier sur un pc
    f=  open("/home/robot/distanceData.txt", "w")
    for i in range(nbPas):
        f.write(str(tabloDistance[i]))
        f.write('\n')  

    print_display(display,  'Exec terminée')
    time.sleep(7)




# When this module is called, it starts the main function.
if __name__ == "__main__":
    main()