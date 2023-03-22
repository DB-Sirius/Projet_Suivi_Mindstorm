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


DistPerRevolution = 1 #Distance parcouru en cm pour une rotation des roues
                      #TODO : Mesurer cette valeur
def clear_display(display):
    display.clear()
    display.update()

def print_display(display, text):
    # using display.text_grid(text, ...) instead of print(test)
    display.text_grid(text, True, 0, 10) # clear screen, 11th row / 22
    display.update()

#fonction qui fait tourner le robot par pas vers la droite de l'angle indiqué
def tournerDroite(angle, gyro, steer_motors):
    values_gyro_init = gyro.angle_and_rate
    values_gyro_actual = gyro.angle_and_rate
    while(values_gyro_actual[0] < values_gyro_init[0] + angle): #tant qu'on est pas à l'angle de décalage demandé
        #si on a plus de 5 degrés avant d'arriver à l'angle cible, on va vite
        if(values_gyro_init[0] + angle -values_gyro_actual[0] > 5):
            steer_motors.on(-100, 5)    
        else: #sinon, on va lentement pour ne pas dépasser l'angle de peu
            steer_motors.on(-100, 1)
        time.sleep(0.5)
        steer_motors.off()
        values_gyro_actual = gyro.angle_and_rate

    #TODO : mettre un mécanisme de correction (retour en arriere) si on dépasse l'angle d'un certain seuil (genre 4-5°)


#Fait avancer le robot en direction d'un angle sur une distance donné
def walkTowardAngle(angle, distance):
    return;

def findTabsDifference(tab1, tab2, errorMarge):
    differenceTab = []
    for i in range(0,len(tab1)) :
        if(errorMarge<1): #Si la valeur fournit est inférieur à 1, on utilise un système de pourcent
            max = tab2[i]*(1+(errorMarge*0.01))
            min = tab2[i]*(1-(errorMarge*0.01))
        else :
            max = tab2[i]+errorMarge
            min = tab2[i]-errorMarge
        print("Max : " + str(max))
        print("Min : " + str(min))
        print("Value : " + str(tab1[i]))
        if((tab1[i]<min)or(tab1[i]>max)):
            print("Found difference at " + str(i) + "th cell, value1 : " + str(tab1[i]) + " different from value2 : " + str(tab2[i]))
            differenceTab.append((i,tab1[i],tab2[i]))
    return differenceTab




def main(noisy = True):
    display = Display()
    us_sensor = UltrasonicSensor()
    steer_motors = MoveSteering(OUTPUT_A, OUTPUT_D)
    tank = MoveTank(OUTPUT_A,OUTPUT_D)
    tank.gyro = GyroSensor()
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
    tank.gyro.calibrate()
    time.sleep(1)
    tabloDistance = []
    tabloDistanceGyro = []
    print_display(display,  'Début scan')
    time.sleep(2)

    #Boucle principale de scan
    for i in range(nbPas):
        gyroValues = tank.gyro.angle_and_rate
        dist = us_sensor.distance_centimeters
        print_display(display,'Pas numero : ' + str(i) + "/ Angle :" + str(gyroValues[0]) + "/Distance: " + str(dist) )
        tabloDistance.append(dist)
        #tabloDistanceGyro.append(gyroValues[0],dist)
        tank.turn_right(5, 10, brake=True, error_margin=2, sleep_time=0.01)
        time.sleep(0.5)

    tank.follow_gyro_angle(
        kp=11.3, ki=0.05, kd=3.2,
        speed=SpeedPercent(30),
        target_angle=180,
        follow_for=follow_for_ms,
        ms=4500
    )

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