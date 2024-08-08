from models.sorting import Sorting

class HandOrganizer:
    def __init__(self, game_state):
        self.game_state = game_state

    def get_sorted_player_hand(self):
        return Sorting.sort_cards(self.game_state.get_player_hand())

    def get_sorted_opponent_hand(self):
        return Sorting.sort_cards(self.game_state.get_opponent_hand())