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

#Fait avancer le robot d'une distance donné en cm
def moveDistance(distance,us_sensor,steer_motors,display):
    moveDuration = distance/7.5 #TODO : Mesurer la distance parcouru en fonction de la duré de rotation, utiliser un nombre de révolution pourrait aussi être pertinent

    steer_motors.on_for_seconds(0,-20,moveDuration)

#Fait tourner le robot d'une valeur donnée en degré
def rotateAngle(angle,gyro,steer_motors,display):
    rotationDuration = ((0.278 * 36)/360)*angle
    steer_motors.on_for_seconds(100, 20, rotationDuration)

#Fait avancer le robot en direction d'un angle sur une distance donné
def moveTowardAngle(angle, distance):
    return

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

def scanEnvironnement(nbPas,us_sensor,steer_motors,display) :
    tabloDistance = []
    rotationDuration = (0.277/36)*nbPas
    for i in range(nbPas):
        dist = us_sensor.distance_centimeters
        print_display(display," Distance: " + str(dist) )
        tabloDistance.append(dist)
        #tabloDistanceGyro.append(gyroValues[0],dist)
        steer_motors.on_for_seconds(100,20,rotationDuration)
        time.sleep(0.24)

    return tabloDistance

def trimTab(tab, max):
    for i in range(0, len(tab)) :
        if tab[i]>max :
            tab[i]=max
    return tab

def findTarget(tab1,tab2, errorMarge):
        differenceTab = findTabsDifference(tab1, tab2, errorMarge)
        for diff in differenceTab :
            if((diff[1]-diff[2])>0):
                return diff

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
    print_display(display,  'Début scan')
    time.sleep(2)



    #moveDistance(15, us_sensor, steer_motors, display) bouge de 15cm


    tabloDistance = scanEnvironnement(nbPas,us_sensor,steer_motors,display)
    tabloDistance = trimTab(tabloDistance,155)

    #Boucle scan 1
    #for i in range(nbPas):
    #    dist = us_sensor.distance_centimeters
    #    print_display(display,'Pas numero : ' + str(i) + "\n Angle :" + str(dist) + "\n Distance: " + str(dist) )
    #    tabloDistance.append(dist)
        #tabloDistanceGyro.append(gyroValues[0],dist)
    #    steer_motors.on_for_seconds(100,20,0.278)

    #    time.sleep(0.2)

    #On dump le tableau des distances dans un txt pour pouvoir les rapatrier sur un pc
    f=  open("/home/robot/distanceData1.txt", "w")
    for i in range(nbPas):
        f.write(str(tabloDistance[i]))
        f.write('\n')  
    f.close()

    tabloDistance2 = scanEnvironnement(nbPas,us_sensor,steer_motors,display)
    tabloDistance2 = trimTab(tabloDistance2,155)

    #boucle scan 2

    #On dump le tableau des distances dans un txt pour pouvoir les rapatrier sur un pc
    f=  open("/home/robot/distanceData2.txt", "w")
    for i in range(nbPas):
        f.write(str(tabloDistance2[i]))
        f.write('\n')
    f.close()


    tabdiff = findTabsDifference(tabloDistance,tabloDistance2, 10)
    f=  open("/home/robot/tableauDiff.txt", "w")
    angleCible = 10 * findTarget(tabloDistance,tabloDistance2, 10)
    f.write("angle: " + str(angleCible))
    f.write('\n')
    for i in range(len(tabdiff)):
        f.write(str("I: " + str(tabdiff[i][0])))
        f.write(str(" T1 : " + str(tabdiff[i][1])))
        f.write(str(" T2 :" + str(tabdiff[i][2])))

        f.write('\n')
    f.close()

    
    

    print_display(display, "angle cible: " + str(angleCible))
    time.sleep(7)




# When this module is called, it starts the main function.
if __name__ == "__main__":
    main()