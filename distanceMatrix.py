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



def main(noisy = True):
    display = Display()
    us_sensor = UltrasonicSensor()
    steer_motors = MoveSteering(OUTPUT_A, OUTPUT_D)
    os.system('setfont Lat15-TerminusBold14')
    
    #Valeur du pas (en degrés)
    step = 10 #N'UTILISER QUE DES DIVISEURS DE 360!!!!
    if(360//step != 0):
        print_display(display,  'Pas invalide')
        time.sleep(2)
        exit()
    nbCases = 360/step

    #Vitesse de rotation
    steer = 10

    tabloDistance = []
    print_display(display,  'Début scan')
    #Boucle principale de scan
    for i in range(nbCases):
        dist = us_sensor.distance_centimeters
        print_display(display,  'Distance: ' + str(dist) )

        tabloDistance[i] = dist

        steer_motors.on(steer, speed) #TODO : comprendre comment ça marche
        time.sleep(2)
        steer_motors.off()

        time.sleep(0.5)

    #On dump le tableau des distances dans un txt pour pouvoir les rapatrier sur un pc
    with open("/home/robot/distanceData.txt", "w") as txt_file:
        for line in tabloDistance:
            txt_file.write(" ".join(line) + "\n")


    
    



# When this module is called, it starts the main function.
if __name__ == "__main__":
    main()