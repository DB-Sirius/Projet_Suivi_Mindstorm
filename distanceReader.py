#!/usr/bin/env python3

import turtle
import time
import sys

step = 10 # Valeur par défaut de scan du robot, en degrés
multiplicateur = 1 # Adapte la taille du cercle à l'écran, à modifier si l'environnement est trop grand ou écran de trop basse résolution

# Lecture tableau 1 depuis .txt
tablo1 = []
f = open('distanceData1.txt','r')
lines = f.readlines()
i = 0
for line in lines:
    tablo1.append(round(float(line))) #convertit en float puis en integer (pour turtle)
    i = i+1
f.close()

# Lecture tableau 2 depuis .txt
tablo2 = []
f = open('distanceData2.txt','r')
lines = f.readlines()
i = 0
for line in lines:
    tablo2.append(round(float(line))) #convertit en float puis en integer (pour turtle)
    i = i+1
f.close()

# Grosso modo écrit comme du GCODE
# Initialisation
turtle.left(90)
turtle.up()
currentValue = tablo1[0]
turtle.forward(multiplicateur*currentValue) #toutes les valeurs de distance seront multipliées par 5
turtle.left(90)
turtle.down()
turtle.color("green")
turtle.speed('fastest')

# Dessin du cercle
# Utilise une approximation du cercle par un polygone à 36 côtés
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
    turtle.forward(multiplicateur*2*3.14159265*currentValue / (360/step)) #approximation de la longueur d'un côté, par 2*pi*R
    turtle.left(step)

# Initialisation pour scan 2
turtle.up()
turtle.goto(0,multiplicateur*tablo2[0])
turtle.down()
turtle.color("red")
currentValue = tablo2[0]

# Scan 2
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
    turtle.forward(multiplicateur*2*3.14159265*currentValue / (360/step)) #approximation de la longueur d'un côté, par 2*pi*R
    turtle.left(step)

time.sleep(30) # Laisse un peu affiché puis ferme, pour ne pas avoir à fermer depuis le terminal