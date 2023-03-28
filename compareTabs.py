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
            if ((diff[1] - diff[2]) > 0):  # On verifie que la distance est négative pour s'assurer qu'il s'agit d'un objet plus proche que le premier scan
                # pour bien detecter la nouvel position de la cible
                # On verifie si les valeur sont proche du relevé précédent pour évaluer si il s'agit du même objet
                if (currentStreak!=[]and(
                        #(diff[1] >= (currentStreak[-1][1] - streakErrorMarge)) and (
                        #diff[1] <= (currentStreak[-1][1] + streakErrorMarge))) and
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
            else: #Si la différence est positive on arrête la streak et on regarde si elle est mieux
                if ((streakCounter > bestStreakCounter)and(streakCounter>0)):
                    print(bestStreak)
                    bestStreakCounter = streakCounter
                    bestStreak = currentStreak.copy()
                currentStreak.clear()
                streakCounter = 0
        #On verifie si la dernière streak est mieux que celle précédement trouvé
        if streakCounter > bestStreakCounter:
            bestStreakCounter = streakCounter
            bestStreak = currentStreak.copy()
        #print(bestStreak)
        print(bestStreakCounter)
        if(len(bestStreak)>0):
            return bestStreak[int(bestStreakCounter / 2)]  #On renvoie l'angle au milieu des angle correspondant à la plus grand streak
        else:
            return bestStreak


def main():
    tab1 = [100, 100, 100, 100, 100, 50, 100, 100, 100, 200, 200, 200]
    tab2 = [100, 100, 100, 40, 50, 100, 50 , 55 , 45 , 50 , 50 , 50]

    print("zzzzzzzzzzz")

    tab4 = [100, 100, 100, 100, 100, 50, 100, 100, 100, 200, 200, 200]

    tab5 = [100, 100, 100, 100, 100, 50, 100, 100, 100, 200, 200, 200]

    tab6 = [100, 100, 100, 100, 40, 50, 100, 100, 100, 200, 200, 200]


    tab3 = []
    target = findTarget(tab1,tab4,10)
    print(target)


# When this module is called, it starts the main function.
if __name__ == "__main__":
    main()