import random
from models.card import Card

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in range(1, 14) for suit in "CDHS"]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if self.cards:
            return self.cards.pop()
        return None