#!/usr/bin/env python3

import turtle
import time
import sys

print(sys.argv)

step = 10
multiplicateur = 0.5

#lecture tableau 1
tablo1 = []
f = open('distanceData1.txt','r')
lines = f.readlines()
i = 0
for line in lines:
    tablo1.append(round(float(line))) #convertit en float puis en integer (pour turtle)
    i = i+1
f.close()

#lecture tableau 2
tablo2 = []
f = open('distanceData2.txt','r')
lines = f.readlines()
i = 0
for line in lines:
    tablo2.append(round(float(line))) #convertit en float puis en integer (pour turtle)
    i = i+1
f.close()

#grosso modo écrit comme du GCODE
#initialisation
turtle.left(90)
turtle.up()
currentValue = tablo1[0]
turtle.forward(multiplicateur*currentValue) #toutes les valeurs de distance seront multipliées par 5
turtle.left(90)
turtle.down()
turtle.color("green")
turtle.speed('fastest')

#dessin du cercle
for i in range(len(tablo1)):
    print(tablo1[i])
    if(tablo1[i]<currentValue): #correction de la position
        turtle.left(90)
        turtle.up()
        turtle.forward(multiplicateur*(currentValue - tablo1[i]))
        turtle.down()
        turtle.right(90)
    if(tablo1[i]>currentValue): #correction de la position
        turtle.right(90)
        turtle.up()
        turtle.forward(multiplicateur*(tablo1[i] - currentValue))
        turtle.down()
        turtle.left(90)

    currentValue = tablo1[i]
    turtle.forward(multiplicateur*2*3.14*currentValue / (360/step)) #approximation de la longueur d'un côté, par 2*pi*R
    turtle.left(step)

turtle.up()
turtle.goto(0,multiplicateur*tablo2[0])
turtle.down()
turtle.color("red")
currentValue = tablo2[0]

for i in range(len(tablo2)):
    print(tablo2[i])
    if(tablo2[i]<currentValue): #correction de la position
        turtle.left(90)
        turtle.up()
        turtle.forward(multiplicateur*(currentValue - tablo2[i]))
        turtle.down()
        turtle.right(90)
    if(tablo2[i]>currentValue): #correction de la position
        turtle.right(90)
        turtle.up()
        turtle.forward(multiplicateur*(tablo2[i] - currentValue))
        turtle.down()
        turtle.left(90)

    currentValue = tablo2[i]
    turtle.forward(multiplicateur*2*3.14*currentValue / (360/step)) #approximation de la longueur d'un côté, par 2*pi*R
    turtle.left(step)

time.sleep(30)