class Card:
    suits = {'C': 0, 'D': 1, 'H': 2, 'S': 3}  # Suit order

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit.upper()  # Ensure suit is uppercase
        self.rank_value = self.calculate_rank_value()
        self.value = min(self.rank_value, 10)  # Card value is the floor of rank value and 10

    def calculate_rank_value(self):
        return min(self.rank, 10)

    def __lt__(self, other):
        return (self.rank_value, Card.suits[self.suit]) < (other.rank_value, Card.suits[other.suit])

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return f"Card(rank='{self.rank}', suit='{self.suit}')"