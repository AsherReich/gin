import logging
from utils.melds_and_deadwood import calculate_optimal_melds_and_deadwood

class Hand:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards
        self.sort_hand()
        self.update_melds_and_deadwood()
        #logging.debug(f"hand class - Hand initialized with cards: {self.cards}")

    def add_card(self, card):
        self.cards.append(card)
        self.sort_hand()
        self.update_melds_and_deadwood()
        logging.debug(f"Card added: {card}")

    def remove_card(self, card):
        self.cards.remove(card)
        self.sort_hand()
        self.update_melds_and_deadwood()
        #logging.debug(f"Card removed: {card}. Hand now: {self.cards}")

    def sort_hand(self):
        self.cards.sort(key=lambda card: (card.rank, card.suit))
        #logging.debug(f"Hand sorted: {self.cards}")

    def update_melds_and_deadwood(self):
        self.melds, self.deadwood = calculate_optimal_melds_and_deadwood(self.cards)
        #logging.debug(f"[Hand] Melds: {[[str(card) for card in meld] for meld in self.melds]}, Deadwood: {[str(card) for card in self.deadwood]}")

    def get_cards(self):
        return self.cards

    def get_melds(self):
        return self.melds

    def get_deadwood(self):
        return self.deadwood

    def calculate_deadwood_value(self):
        return sum(card.value for card in self.deadwood)