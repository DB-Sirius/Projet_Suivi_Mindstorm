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
from PIL             import Image


# Efface l'écran
def clear_display(display):
    display.clear()
    display.update()

# écrit text sur l'écran
def print_display(display, text):
    display.text_grid(text, True, 0, 10)
    display.update()

# Fait avancer le robot d'une distance donnée en cm vers l'avant
def moveDistance(distance,steer_motors,display):
    moveDuration = distance/7.5
    steer_motors.on_for_seconds(0,-20,moveDuration)

# Fait tourner le robot d'une valeur donnée en degré dans le sens trigonométrique
# Prévu pour bouger 10° d'un coup ,sinon probablement pas terrible
def rotateAngle(angle,gyro,steer_motors,display):
    while(angle > 360):
        angle = angle - 360
    while(angle < 0):
        angle = angle + 360
    if(angle <= 180):
        rotationDuration = ((0.278 * 36)/360)*angle
        steer_motors.on_for_seconds(100, 20, rotationDuration)
    else:
        rotationDuration = ((0.278 * 36)/360)*(360 - angle)
        steer_motors.on_for_seconds(-100, 20, rotationDuration)

# Fait avancer le robot en direction d'un angle sur une distance donnée
def moveTowardAngle(angle, distance, gyro, steer_motors, display):
    #on s'oriente vers l'angle recherché, si possible multiple de 10°
    while(angle > 360):
        angle = angle - 360
    while(angle < 0):
        angle = angle + 360
    rotateAngle(angle,gyro,steer_motors,display)
    moveDistance(distance,steer_motors,display)
    return

# Fonction de correction de l'angle pour une rotation plus précise
# Non utilisé dans la version finale, le gyro pose plus de problèmes qu'il n'en corrige
def correctAngle(angleCible, gyro, steer_motors, display):
    values_gyro = gyro.angle_and_rate
    correction = values_gyro[0] - angleCible
    print_display(display,  "correction angle : " + str(correction))
    rotateAngle(correction,gyro,steer_motors,display)
    return


# Fonction qui fait tourner le robot à 360° et mesure les distances aux obstacles
# nbPas : nombre de pas à faire par tour
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

# Tronque les valeurs > max du tableau
def trimTab(tab, max):
    for i in range(0, len(tab)) :
        if tab[i]>max :
            tab[i]=max
    return tab


def findTarget(tab1, tab2, errorMarge, closestValue = False):
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
                    (diff[2] >= (currentStreak[-1][2] - streakErrorMarge)) and (
                    diff[2] <= (currentStreak[-1][1] + streakErrorMarge)))):
                # Si c'est le cas on ajoute 1 au compteur d'angle reprsentant cet objet
                streakCounter += 1
                # et on ajoute cet angle à la liste des angles le réprésentant
                currentStreak.append(diff)
            # Sinon on créé une nouvelle streak
            else:
                # On sauvegarde avant l'ancienne streak si la nouvelle est plus grand
                if streakCounter > bestStreakCounter:
                    bestStreakCounter = streakCounter
                    bestStreak = currentStreak.copy()
                streakCounter = 1
                currentStreak.clear()
                currentStreak.append(diff)
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
        return bestStreak[int(bestStreakCounter / 2)]  # On renvoie l'angle au milieu des angle correspondant à la plus grand streak
    else:
        return bestStreak


# Fonction pour trouver la plus grande différence dans deux tableaux de distance
# Utilisée pour détecter le changement de position de la cible, en s'appuyant exclusivement sur les données de scan
# Marge d'erreur en cm
# Renvoie un tableau de tuples avec (Index de la cellule où se trouve la différence,valeur du premier tableau, valeur du deuxième tableau)
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
    
    nbPas = 36
    writeInFiles = True #controle si on dump les tableaux dans un txt

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

        values_gyro = tank.gyro.angle_and_rate
        angleControle = values_gyro[0] #on prend l'angle de controle pour le corriger plus tard

        tabloDistance = scanEnvironnement(nbPas,us_sensor,steer_motors,display)
        tabloDistance = trimTab(tabloDistance,155)

        time.sleep(0.5)
        #correctAngle(angleControle, tank.gyro, steer_motors, display) #correction de l'angle en théorie, mais foirée

        tabloDistance2 = scanEnvironnement(nbPas,us_sensor,steer_motors,display)
        tabloDistance2 = trimTab(tabloDistance2,155)

        tabdiff = findTabsDifference(tabloDistance,tabloDistance2, 10)
        target = findTarget(tabloDistance,tabloDistance2, 10)
        angleCible = 10 * target[0]

        time.sleep(0.5)
        moveTowardAngle(angleCible, target[2]-5, tank.gyro, steer_motors, display)


        # Ecriture éventuelle des fichiers pour le débug
        if(writeInFiles):
            # Premier scan
            f=  open("/home/robot/distanceData1.txt", "w")
            for i in range(nbPas):
                f.write(str(tabloDistance[i]))
                f.write('\n')  
            f.close()

            #Second scan
            f=  open("/home/robot/distanceData2.txt", "w")
            for i in range(nbPas):
                f.write(str(tabloDistance2[i]))
                f.write('\n')
            f.close()

            # Tableau des différences et infos complémentaires
            f=  open("/home/robot/tableauDiff.txt", "w")
            f.write("angle: " + str(angleCible))
            f.write('\n')
            for i in range(len(tabdiff)):
                f.write(str("I: " + str(tabdiff[i][0])))
                f.write(str(" T1 : " + str(tabdiff[i][1])))
                f.write(str(" T2 :" + str(tabdiff[i][2])))

                f.write('\n')
            f.write('anglecible : '+str(angleCible))
            f.close()
        
        time.sleep(2)

    
    
    time.sleep(7)




# When this module is called, it starts the main function.
if __name__ == "__main__":
    main()