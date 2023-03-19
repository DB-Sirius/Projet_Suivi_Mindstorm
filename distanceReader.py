"""
PROGRAMME À EXECUTER SUR PC, QUI LIT LES DONNÉES RENVOYÉES PAR LE ROBOT
"""

import turtle
import time
import sys

print(sys.argv)
#TODO : importer le tableau de données
#TODO : importer les arguments suivants au lieu de les coder en dur : le step, et le tableau
step = 10
tablo = [i for i in range(36)]


#grosso modo écrit comme du GCODE
#initialisation
turtle.left(90)
turtle.up()
currentValue = tablo[0]
turtle.forward(10*currentValue) #toutes les valeurs de distance seront multipliées par 5
turtle.right(90)
turtle.down()

#dessin du cercle
for i in range(len(tablo)):
    if(tablo[i]<currentValue): #correction de la position
        turtle.right(90)
        turtle.forward(10*(currentValue - tablo[i]))
        turtle.left(90)
    if(tablo[i]>currentValue): #correction de la position
        turtle.left(90)
        turtle.forward(10*(tablo[i] - currentValue))
        turtle.right(90)

    currentValue = tablo[i]
    turtle.forward(10*2*3.14*currentValue / (360/step)) #approximation de la longueur d'un côté, par 2*pi*R
    turtle.right(step)
    



time.sleep(5)