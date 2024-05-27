import random
from models.observable import Observable
from models.deck import Deck

class GameState(Observable):
    def __init__(self):
        super().__init__()
        self.current_turn = 'player'
        self.has_drawn_card = False
        self.has_discarded_card = False
        self.deck = Deck()        
        self.player_hand = []
        self.opponent_hand = []
        self.draw_pile = []
        self.discard_pile = []
        self.scores = {'player': 0, 'opponent': 0}
        self.selected_card = None
        self.reset_game()

    def draw_card(self, player, from_discard=False):
        card = None
        if from_discard and self.discard_pile:
            card = self.discard_pile.pop()
        elif self.draw_pile:
            card = self.draw_pile.pop()
        
        if card:
            if player == 'player':
                self.player_hand.append(card)
            else:
                self.opponent_hand.append(card)
            self.has_drawn_card = True
            self.notify_observers()
        return card

    def discard_card(self, card):
        if self.current_turn == 'player':
            if card in self.player_hand:
                self.player_hand.remove(card)
        else:
            if card in self.opponent_hand:
                self.opponent_hand.remove(card)
        
        self.discard_pile.append(card)
        self.has_discarded_card = True
        self.notify_observers()

    def select_card(self, card):
        self.selected_card = card
        self.notify_observers()

    def switch_turn(self):
        self.current_turn = 'opponent' if self.current_turn == 'player' else 'player'
        self.has_drawn_card = False
        self.has_discarded_card = False

    def reset_round(self):
        self.current_turn = 'player'
        self.has_drawn_card = False
        self.has_discarded_card = False
        self.player_hand.clear()
        self.opponent_hand.clear()
        self.draw_pile = self.deck.cards.copy()
        random.shuffle(self.draw_pile)
        self.discard_pile.clear()
        self.deal_initial_hands()
        self.notify_observers()

    def deal_initial_hands(self):
        self.player_hand = [self.draw_pile.pop() for _ in range(10)]
        self.opponent_hand = [self.draw_pile.pop() for _ in range(10)]
        self.discard_pile.append(self.draw_pile.pop())

    def reset_game(self):
        self.scores = {'player': 0, 'opponent': 0}
        self.reset_round()

    # Getter methods
    def get_current_turn(self):
        return self.current_turn

    def has_player_drawn_card(self):
        return self.has_drawn_card

    def has_player_discarded_card(self):
        return self.has_discarded_card

    def get_player_hand(self):
        return self.player_hand

    def get_opponent_hand(self):
        return self.opponent_hand

    def get_draw_pile(self):
        return self.draw_pile

    def get_discard_pile(self):
        return self.discard_pile

    def get_scores(self):
        return self.scores

    def get_selected_card(self):
        return self.selected_card