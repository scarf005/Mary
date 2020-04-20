import random
from data import INVENTORY_ORDER

#create inventory class
class Inventory:
    def __init__(self, capacity = 10):
        self.capacity = capacity
        self.holding = []

    #Describes whole inventory.
    def Show(self):
        if len(self.holding) >= 1:
            print("your inventory:")
            j = 0
            for i in self.holding:
                num = INVENTORY_ORDER[j]
                print(f"{num} {i.name}")
                j += 1
        else:
            print("your inventory is empty.")

    #Show how much item is in the inventory (Maybe it's not that useful at all)
    def ShowNum(self, item):
        for i in self.holding:
            print(i)
            print(i.name)
        """
        if item in self.holding:
            j = 0
            for i in self.holding:
                if i == showwhich:
                    j += 1
                    print("you have {n} {item} in your inventory.".format(j,showwhich))
        else:
            print("You do not have any {item} in your inventory.".format(item))
        """

    #WIP: first get some decent search function
    """
    #Explain items (if possible)               
    def Explain(self, item):
        try:
            if how_much_items_in(item, self.holding):
                print("at least it exsists")
                print(item.Show())
        except:
            print("It's got nothing to say about itself.")

    def Quaff(self,item):
        if item.content == "acid":
            print("Arrrgh! the acid burns!")
        elif item.content == "regen":
            print("you feel much better.")
        else:
            print("There's nothing you can do with {item}.".format(item))

    """
    def Add(self, item):
        #add
        self.holding.append(item)

    def Remove(self, key):
        #알파벳을 인수로 받고, 거기에 해당하는 번호를 지움. 글로 써 보니 생각보다 간단하네.
        number = INVENTORY_ORDER.find(key)
        del self.holding[number]


#Search in Inventory

"""
def how_much_items_in(find, lists):
    j = 0
    for i in lists:
        if find == lists:
            j += 1
    if j == 0:
        return False
    else:
        return j
"""