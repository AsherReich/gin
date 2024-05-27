class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        print(f"Card created: {self.rank}{self.suit}")

    def __str__(self):
        return f"{self.rank}{self.suit.upper()}"

    def __repr__(self):
        return self.__str__()