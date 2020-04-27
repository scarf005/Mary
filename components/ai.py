class BasicMonster:
    def take_turn(self, message):
        message.log(F'The {self.owner.name} wonders when it will get to move')