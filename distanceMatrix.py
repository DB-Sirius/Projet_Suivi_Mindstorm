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

#fonction qui fait tourner le robot par pas vers la droite de l'angle indiqué
def tournerDroite(angle, gyro, steer_motors, display):
    values_gyro_init = gyro.angle_and_rate
    values_gyro_actual = gyro.angle_and_rate
    compteurPas = 0
    while(values_gyro_actual[0] < values_gyro_init[0] + angle): #tant qu'on est pas à l'angle de décalage demandé
        #si on a plus de 5 degrés avant d'arriver à l'angle cible, on va vite
        if(values_gyro_init[0] + angle -values_gyro_actual[0] > 5):
            steer_motors.on(-100, 5)    
        else: #sinon, on va lentement pour ne pas dépasser l'angle de peu
            steer_motors.on(-100, 3)
        time.sleep(0.5)
        steer_motors.off()
        values_gyro_actual = gyro.angle_and_rate
        print_display(display,'rotation numero : ' + str(compteurPas) + "/ Angle :" + str(values_gyro_actual[0]))
        
        compteurPas = compteurPas+1

    #TODO : mettre un mécanisme de correction (retour en arriere) si on dépasse l'angle d'un certain seuil (genre 4-5°)

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

#Renvoie un tableau de tuples avec (Index de la cellule où se trouve la différence,valeur du premier tableau, valeur du deuxième tableau)
def findTabsDifference(tab1, tab2, errorMarge):
    differenceTab = []
    for i in range(0,len(tab1)) :
        if(errorMarge<1): #Si la valeur fournit est inférieur à 1, on utilise un système de pourcent
            max = tab2[i]*(1+(errorMarge*0.01))
            min = tab2[i]*(1-(errorMarge*0.01))
        else :
            max = tab2[i]+errorMarge
            min = tab2[i]-errorMarge
        if((tab1[i]<min)or(tab1[i]>max)):
            differenceTab.append((i,tab1[i],tab2[i]))
    return differenceTab


def main(noisy = True):
    display = Display()
    us_sensor = UltrasonicSensor()
    steer_motors = MoveSteering(OUTPUT_A, OUTPUT_D)
    gyro_sensor = GyroSensor()
    os.system('setfont Lat15-TerminusBold14')
    
    #Valeur du pas (en degrés)
    step = 10 #N'UTILISER QUE DES DIVISEURS DE 360!!!!
    if(False): #se démerder pour avoir une condition qui marche
        print_display(display,  'Pas invalide')
        time.sleep(2)
        exit()
    nbCases = 360/step #convertir en entier

    nbPas = 36

    print_display(display,  'CALIBRATION')
    gyro_sensor.calibrate()
    time.sleep(1)

    ################## SCAN 1 #################
    tabloDistance = []
    print_display(display,  'Début scan 1')
    time.sleep(2)

    #Boucle principale de scan
    for i in range(nbPas): 
        dist = us_sensor.distance_centimeters
        #print_display(display,  'Distance: ' + str(dist) )
        tabloDistance.append(dist)
        tournerDroite(10, gyro_sensor, steer_motors, display)
        time.sleep(0.5)

    #On dump le tableau des distances dans un txt pour pouvoir les rapatrier sur un pc
    f=  open("/home/robot/distanceData1.txt", "w")
    for i in range(nbPas):
        f.write(str(tabloDistance[i]))
        f.write('\n')  


    ################## SCAN 2 #################

    tabloDistance = []
    print_display(display,  'Début scan 2')
    time.sleep(2)

    for i in range(nbPas): 
        dist = us_sensor.distance_centimeters
        #print_display(display,  'Distance: ' + str(dist) )
        tabloDistance.append(dist)
        tournerDroite(10, gyro_sensor, steer_motors, display)
        time.sleep(0.5)

    #On dump le tableau des distances dans un txt pour pouvoir les rapatrier sur un pc
    f=  open("/home/robot/distanceData2.txt", "w")
    for i in range(nbPas):
        f.write(str(tabloDistance[i]))
        f.write('\n')  

    print_display(display,  'Exec terminée')
    time.sleep(7)


    '''
    Mettre ici le code pour qu'il aille dans le bon sens apres avoir vu les différences
    '''


# When this module is called, it starts the main function.
if __name__ == "__main__":
    main()