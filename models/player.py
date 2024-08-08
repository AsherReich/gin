from models.hand import Hand

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def get_hand(self):
        return self.hand