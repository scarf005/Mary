from data import *

class Potion:
    def __init__(self,content,appearance,identified=False):
        self.content = content
        self.appearance = appearance
        self.identified = identified
        self.name = "potion of {0}".format(content)

    def Show(self):
        if self.identified == True:
            return "This bottle contains potion of {0}.".format(self.content)
        else:
            return "This bottle contains {0} liquid.".format(self.appearance)