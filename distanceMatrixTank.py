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
def moveDistance(distance,steer_motors,display):
    moveDuration = distance/7.5
    steer_motors.on_for_seconds(0,-20,moveDuration)

#Fait tourner le robot d'une valeur donnée en degré
#prévu pour bouger 10° d'un coup ,sinon probablement pas terrible
def rotateAngle(angle,gyro,steer_motors,display):
    if(angle <= 180):
        rotationDuration = ((0.278 * 36)/360)*angle
        steer_motors.on_for_seconds(100, 20, rotationDuration)
    else:
        rotationDuration = ((0.278 * 36)/360)*(360 - angle)
        steer_motors.on_for_seconds(-100, 20, rotationDuration)

#Fait avancer le robot en direction d'un angle sur une distance donné
def moveTowardAngle(angle, distance, gyro, steer_motors, display):
    #on s'oriente vers l'angle recherché, si possible multiple de 10°
    while(angle > 360):
        angle = angle - 360
    rotateAngle(angle,gyro,steer_motors,display)
    #On avance
    moveDistance(distance,steer_motors,display)
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


#Fonction ayant pour but de trouvé un suite d'angle ayant une différence négative entre le premier et le deuxième scan
#pour trouver la position de la cible
def findTarget(tab1, tab2, errorMarge):
    differenceTab = findTabsDifference(tab1, tab2, errorMarge)
    print(differenceTab)
    currentStreak = []
    bestStreak = []
    streakCounter = 0
    bestStreakCounter = -1
    streakErrorMarge = errorMarge + 5
    for diff in differenceTab:
        if ((diff[1] - diff[
            2]) > 0):  # On verifie que la distance est négative pour s'assurer qu'il s'agit d'un objet plus proche que le premier scan
            # pour bien detecter la nouvel position de la cible
            # On verifie si les valeur sont proche du relevé précédent pour évaluer si il s'agit du même objet
            if (currentStreak != [] and (
                    # (diff[1] >= (currentStreak[-1][1] - streakErrorMarge)) and (
                    # diff[1] <= (currentStreak[-1][1] + streakErrorMarge))) and
                    (diff[2] >= (currentStreak[-1][2] - streakErrorMarge)) and (
                    diff[2] <= (currentStreak[-1][1] + streakErrorMarge)))):
                # Si c'est le cas on ajoute 1 au compteur d'angle reprsentant cet objet
                streakCounter += 1
                # et on ajoute cet angle à la liste des angles le réprésentant
                currentStreak.append(diff)
            # Sinon on créé une nouvelle streak
            else:
                currentStreak.clear()
                currentStreak.append(diff)
                # On sauvegarde avant l'ancienne streak si la nouvelle est plus grand
                if streakCounter > bestStreakCounter:
                    bestStreakCounter = streakCounter
                    bestStreak = currentStreak.copy()
                streakCounter = 1
            print(currentStreak)
        else:  # Si la différence est positive on arrête la streak et on regarde si elle est mieux
            if ((streakCounter > bestStreakCounter) and (streakCounter > 0)):
                print(bestStreak)
                bestStreakCounter = streakCounter
                bestStreak = currentStreak.copy()
            currentStreak.clear()
            streakCounter = 0
    # On verifie si la dernière streak est mieux que celle précédement trouvé
    if streakCounter > bestStreakCounter:
        bestStreakCounter = streakCounter
        bestStreak = currentStreak.copy()
    # print(bestStreak)
    print(bestStreakCounter)
    if (len(bestStreak) > 0):
        return bestStreak[
            int(bestStreakCounter / 2)]  # On renvoie l'angle au milieu des angle correspondant à la plus grand streak
    else:
        return bestStreak

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
    #traitement des différences pour ne garder que celles où 2 pts consécutifs sont significatifs
    differenceCorrected = []
    for j in range(0, len(differenceTab)-1):
        if(differenceTab[j][0] == differenceTab[j+1][0] - 1):
            differenceCorrected.append(differenceTab[j]) #on renvoie la premiere case lorsqu'il y a 2 pts, donc utiliser +10° lors du choix de l'angle
    return differenceCorrected


def main(noisy = True):
    display = Display()
    us_sensor = UltrasonicSensor()
    steer_motors = MoveSteering(OUTPUT_A, OUTPUT_D)
    tank = MoveTank(OUTPUT_A,OUTPUT_D)
    tank.gyro = GyroSensor()
    os.system('setfont Lat15-TerminusBold14')
    
    #Valeur du pas (en degrés)
    step = 10 #N'UTILISER QUE DES DIVISEURS DE 360!!!!
    nbPas = 36
    writeInFiles = False #controle si on dump les tableaux dans un txt

    #Séquence au démarrage
    print_display(display,  'CALIBRATION')
    tank.gyro.calibrate()
    time.sleep(1)
    tabloDistance = []
    print_display(display,  "Début de l'exécution")
    time.sleep(2)

    compteurExecutions = 0

    while(True):
        compteurExecutions = compteurExecutions+1
        print_display(display,  'Execution ' + str(compteurExecutions))

        tabloDistance = scanEnvironnement(nbPas,us_sensor,steer_motors,display)
        tabloDistance = trimTab(tabloDistance,155)

        tabloDistance2 = scanEnvironnement(nbPas,us_sensor,steer_motors,display)
        tabloDistance2 = trimTab(tabloDistance2,155)

        tabdiff = findTabsDifference(tabloDistance,tabloDistance2, 10)
        target = findTarget(tabloDistance,tabloDistance2, 10)
        angleCible = 10 * target[0]

        moveTowardAngle(angleCible, target[1], tank.gyro, steer_motors, display)



        if(writeInFiles):
            f=  open("/home/robot/distanceData1.txt", "w")
            for i in range(nbPas):
                f.write(str(tabloDistance[i]))
                f.write('\n')  
            f.close()

            f=  open("/home/robot/distanceData2.txt", "w")
            for i in range(nbPas):
                f.write(str(tabloDistance2[i]))
                f.write('\n')
            f.close()

            f=  open("/home/robot/tableauDiff.txt", "w")
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