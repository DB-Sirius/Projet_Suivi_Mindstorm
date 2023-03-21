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
        print("Max : " + str(max))
        print("Min : " + str(min))
        print("Value : " + str(tab1[i]))
        if((tab1[i]<min)or(tab1[i]>max)):
            print("Found difference at " + str(i) + "th cell, value1 : " + str(tab1[i]) + " different from value2 : " + str(tab2[i]))
            differenceTab.append((i,tab1[i],tab2[i]))
    return differenceTab