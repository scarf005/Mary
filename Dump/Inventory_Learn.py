import random
from inventory import Inventory
from potion import Potion
from data import *

#Setting up 
Inv = Inventory()

random.shuffle(POTION_APPEARANCE)
POTION_DICTIONARY = dict(zip(POTION_CONTENT,POTION_APPEARANCE))

#Main
Acid_Potion = Potion("acid",POTION_DICTIONARY["acid"],True)
Regen_Potion = Potion("regeneration",POTION_DICTIONARY["regeneration"],False)
Juice_Potion = Potion("fruit juice",POTION_DICTIONARY["regeneration"],False)

Inv.Add(Acid_Potion)
Inv.Add(Regen_Potion)
Inv.Add(Juice_Potion)

#Inv.Explain(Acid_Potion)
#Inv.Explain(Regen_Potion)



#Loop about things you can do
while True:
    Inv.Show()
    Answer = input("\nr to remove, x to exit ") 
    if Answer == "x":
        break

    elif Answer == "r":
        Inv.Show()
        Inv.Remove(input("What do you want to remove? (type alphabet) "))

    else:
        print("invalid command.")
    
    """
    elif Answer == "e":
    Inv.Explain(input("explain which? (type alpahbet) "))
    
    elif Answer == "q":
    Inv.Quaff(input("Drink which potion? "))
    
    elif Answer == "a":
        Answer = input("name the item you want to add: ")
        Inv.Add(Answer)
    """
    

