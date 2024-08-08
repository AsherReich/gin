import random
import logging
from models.observable import Observable
from models.deck import Deck
from models.player import Player
from models.hand import Hand

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

class GameState(Observable):
    def __init__(self):
        super().__init__()
        self.current_turn = 'player'
        self.has_drawn_card = False
        self.deck = Deck()
        self.players = {
            'player': Player('player'),
            'opponent': Player('opponent')
        }
        self.draw_pile = []
        self.discard_pile = []
        self.scores = {'player': 0, 'opponent': 0}
        self.selected_card = None
        self.knock_card = None
        self.legal_actions = {"gin": False, "big_gin": False, "knock": False, "draw": True}
        self.reset_game()

    def get_current_player(self):
        return self.players[self.current_turn]

    def draw_card(self, from_discard=False):
        card = None
        if from_discard and self.discard_pile:
            card = self.discard_pile.pop()
            logging.debug(f"[GameState] Drawn from discard pile")

        elif self.draw_pile:
            card = self.draw_pile.pop()
            logging.debug(f"[GameState] Drawn from draw pile")

        if card:
            self.get_current_player().get_hand().add_card(card)
            self.has_drawn_card = True
            self.notify_observers()
        logging.debug(f"[GameState] Drawn: {card}")
        return card

    def discard_card(self, card):
        current_player = self.get_current_player()
        if card in current_player.get_hand().get_cards():
            current_player.get_hand().remove_card(card)
            self.discard_pile.append(card)
        self.has_drawn_card = False
        self.switch_turn()

    def select_card(self, card):
        self.selected_card = card
        self.notify_observers()

    def unselect_card(self):
        self.selected_card = None
        self.notify_observers()

    def switch_turn(self):
        self.current_turn = 'opponent' if self.current_turn == 'player' else 'player'
        self.has_drawn_card = False
        self.notify_observers()

    def reset_round(self):
        self.current_turn = 'player'
        self.has_drawn_card = False
        self.draw_pile = self.deck.cards.copy()
        random.shuffle(self.draw_pile)
        self.discard_pile.clear()
        self.deal_initial_hands()
        self.knock_card = self.draw_pile.pop()
        self.notify_observers()

    def deal_initial_hands(self):
        player_cards = [self.draw_pile.pop() for _ in range(10)]
        opponent_cards = [self.draw_pile.pop() for _ in range(10)]
        self.players['player'].hand = Hand(player_cards)
        self.players['opponent'].hand = Hand(opponent_cards)
        self.discard_pile.append(self.draw_pile.pop())

    def reset_game(self):
        self.scores = {'player': 0, 'opponent': 0}
        self.reset_round()

    def notify_observers(self):
        super().notify_observers()
        player_hand_str = [f"{card.rank}{card.suit.lower()}" for card in self.players['player'].get_hand().get_cards()]
        melds_str = [[f"{card.rank}{card.suit.lower()}" for card in meld] for meld in self.players['player'].get_hand().get_melds()]
        deadwood_str = [f"{card.rank}{card.suit.lower()}" for card in self.players['player'].get_hand().get_deadwood()]
        opponent_hand_str = [f"{card.rank}{card.suit.lower()}" for card in self.players['opponent'].get_hand().get_cards()]
        draw_pile_str = [f"{card.rank}{card.suit.lower()}" for card in self.draw_pile]
        discard_pile_str = [f"{card.rank}{card.suit.lower()}" for card in self.discard_pile]

        logging.debug(f"[GameState] Player hand: {player_hand_str}")
        logging.debug(f"[GameState] Melds: {melds_str}")
        logging.debug(f"[GameState] Deadwood: {deadwood_str}")
        logging.debug(f"[GameState] Opponent hand: {opponent_hand_str}")
        logging.debug(f"[GameState] Discard pile: {discard_pile_str}")
        logging.debug(f"[GameState] Current turn: {self.current_turn}")

    # Getter methods
    def get_current_turn(self):
        return self.current_turn

    def has_player_drawn_card(self):
        return self.has_drawn_card

    def get_player_hand(self):
        return self.players['player'].get_hand()

    def get_opponent_hand(self):
        return self.players['opponent'].get_hand()

    def get_draw_pile(self):
        return self.draw_pile

    def get_discard_pile(self):
        return self.discard_pile

    def get_scores(self):
        return self.scores

    def get_selected_card(self):
        return self.selected_card