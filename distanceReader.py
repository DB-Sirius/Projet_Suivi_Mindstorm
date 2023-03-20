#!/usr/bin/env python3

import turtle
import time
import sys

print(sys.argv)
#TODO : importer le tableau de données
#TODO : importer les arguments suivants au lieu de les coder en dur : le step, et le tableau
step = 10
multiplicateur = 1
tablo = []

f = open('distanceData.txt','r')
lines = f.readlines()
i = 0
for line in lines:
    tablo.append(round(float(line))) #convertit en float puis en integer (pour turtle)
    i = i+1

f.close()

#grosso modo écrit comme du GCODE
#initialisation
turtle.left(90)
turtle.up()
currentValue = tablo[0]
turtle.forward(multiplicateur*currentValue) #toutes les valeurs de distance seront multipliées par 5
turtle.right(90)
turtle.down()

#dessin du cercle
for i in range(len(tablo)):
    print(tablo[i])
    if(tablo[i]<currentValue): #correction de la position
        turtle.right(90)
        turtle.forward(multiplicateur*(currentValue - tablo[i]))
        turtle.left(90)
    if(tablo[i]>currentValue): #correction de la position
        turtle.left(90)
        turtle.forward(multiplicateur*(tablo[i] - currentValue))
        turtle.right(90)

    currentValue = tablo[i]
    turtle.forward(multiplicateur*2*3.14*currentValue / (360/step)) #approximation de la longueur d'un côté, par 2*pi*R
    turtle.right(step)
    



time.sleep(10)