from utils.constants import TARGET_SCORE
from models.game_state import GameState
from views.game_view import GameView

class GameController:

    def __init__(self, game_state, game_view):
        self.game_state = game_state
        self.game_view = game_view
        self.target_score = TARGET_SCORE

    def handle_draw_pile_click(self):
        if self.can_draw():
            self.game_state.draw_card('player')
            self.update_view()

    def handle_discard_pile_click(self):
        if self.can_draw():
            self.game_state.draw_card('player', from_discard=True)
            self.update_view()

    def handle_card_selection(self, card):
        if self.can_discard_card():
            self.game_state.select_card(card)
            self.update_view()

    def handle_card_discard(self, card):
        if self.can_discard_card():
            self.game_state.discard_card(card)
            self.end_turn()

    def can_draw(self):
        return self.game_state.current_turn == 'player' and not self.game_state.has_drawn_card

    def can_discard_card(self):
        return self.game_state.current_turn == 'player' and self.game_state.has_drawn_card

    def end_turn(self):
        self.game_state.switch_turn()
        if self.game_state.current_turn == 'opponent':
            self.ai_turn()
        self.update_view()

    def ai_turn(self):
        card = self.game_state.draw_card('opponent')
        if self.check_for_gin(self.game_state.opponent_hand):
            self.end_round('opponent')
        else:
            card_to_discard = random.choice(self.game_state.opponent_hand)
            self.game_state.discard_card(card_to_discard)
            self.end_turn()

    def check_for_gin(self, hand):
        # Add logic to check for Gin Rummy
        return False

    def end_round(self, winner):
        print(f"Round over! Winner: {winner}")
        self.game_state.reset_round()
        if self.game_state.scores[winner] >= self.target_score:
            self.end_game(winner)
        self.update_view()

    def end_game(self, winner):
        print(f"Game over! Winner: {winner}")
        self.game_state.reset_game()
        self.update_view()

    def update_view(self):
        self.game_view.render(self.game_state)