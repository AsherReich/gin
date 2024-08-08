import random
import logging
from kivy.clock import Clock
from utils.constants import TARGET_SCORE, AI_TIME_DELAY
from utils.game_rules import GameRules
from utils.ending_conditions import EndingConditions

class GameController:
    def __init__(self, game_state, game_view):
        self.AI_TIME_DELAY = AI_TIME_DELAY
        self.game_state = game_state
        self.game_view = game_view

        # Subscribe to events from the view
        self.game_view.bind(on_draw_pile_click=self.handle_draw_pile_click)
        self.game_view.bind(on_discard_pile_click=self.handle_discard_pile_click)
        self.game_view.bind(on_card_single_click=self.handle_card_single_click)
        self.game_view.bind(on_card_double_click=self.handle_card_double_click)
        self.game_view.bind(on_action_button_click=self.handle_legal_action_click)

    def handle_draw_pile_click(self, instance):
        if GameRules.is_action_valid(self.game_state, "draw"):
            self.game_state.draw_card()
            self.update_legal_actions()

    def handle_discard_pile_click(self, instance):
        if GameRules.is_action_valid(self.game_state, "draw"):
            self.game_state.draw_card(from_discard=True)
            self.update_legal_actions()

    def handle_card_single_click(self, instance, card):
        if GameRules.is_action_valid(self.game_state, "discard"):
            if self.game_state.selected_card == card:
                self.game_state.unselect_card()
            else:
                self.game_state.select_card(card)

    def handle_card_double_click(self, instance, card):
        if GameRules.is_action_valid(self.game_state, "discard"):
            self.game_state.discard_card(card)
            self.update_legal_actions()
            self.end_turn()

    def handle_legal_action_click(self, instance, action):
        if GameRules.is_action_valid(self.game_state, action):
            self.end_round(action)

    def update_legal_actions(self):
        self.game_state.legal_actions = GameRules.determine_legal_actions(self.game_state)
        self.game_view.update_legal_actions(self.game_state.legal_actions)

    def end_turn(self):
        self.game_state.switch_turn()
        if self.game_state.current_turn == 'opponent':
            Clock.schedule_once(self.ai_take_turn, self.AI_TIME_DELAY)

    def ai_take_turn(self, dt):
        if self.game_state.legal_actions["draw"]:
            if self.should_draw_from_discard():
                self.game_state.draw_card(from_discard=True)
            else:
                self.game_state.draw_card()
            self.update_legal_actions()
        Clock.schedule_once(self.ai_discard_or_end_round, self.AI_TIME_DELAY)

    def should_draw_from_discard(self):
        # Example AI strategy: Draw from discard pile if the card rank is 5 or less
        if self.game_state.discard_pile:
            return self.game_state.discard_pile[-1].rank <= 5
        return False

    def ai_discard_or_end_round(self, dt):
        legal_actions = self.game_state.legal_actions
        if legal_actions["big_gin"]:
            self.end_round("big_gin")
        elif legal_actions["gin"]:
            self.end_round("gin")
        elif legal_actions["knock"]:
            self.end_round("knock")
        else:
            card_to_discard = random.choice(self.game_state.get_opponent_hand().get_cards())
            self.game_state.discard_card(card_to_discard)
            self.update_legal_actions()
            self.end_turn()

    def end_round(self, action):
        logging.debug(f"Round over! Action: {action}")
        round_winner = self.game_state.current_turn
        round_score = self.calculate_round_score()
        GameRules.update_scores(self.game_state, round_winner, round_score)

        if GameRules.confirm_end_of_round(action):
            self.game_state.reset_round()
        else:
            self.end_game(round_winner)

    def calculate_round_score(self):
        # Implement the logic to calculate the round score based on the game state
        # This is a placeholder example
        return random.randint(10, 50)

    def end_game(self, winner):
        logging.debug(f"Game over! Winner: {winner}")
        self.game_state.reset_game()