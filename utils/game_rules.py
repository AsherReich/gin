from utils.ending_conditions import EndingConditions

class GameRules:
    @staticmethod
    def determine_legal_actions(game_state):
        if GameRules.is_round_over(game_state):
            return {"gin": False, "big_gin": False, "knock": False, "draw": False}

        legal_actions = {"gin": False, "big_gin": False, "knock": False, "draw": False}
        if not game_state.has_drawn_card:
            legal_actions["draw"] = True
        else:
            highest_order_action = EndingConditions.get_highest_order_action(game_state.get_current_hand(), game_state.get_knock_card())
            if highest_order_action:
                legal_actions[highest_order_action] = True
        return legal_actions

    @staticmethod
    def is_round_over(game_state):
        return any([game_state.legal_actions["gin"], game_state.legal_actions["big_gin"], game_state.legal_actions["knock"]])

    @staticmethod
    def is_action_valid(game_state, action):
        return game_state.legal_actions.get(action, False)

    @staticmethod
    def confirm_end_of_round(action):
        return action in ["gin", "big_gin", "knock"]

    @staticmethod
    def update_scores(game_state, round_winner, round_score):
        game_state.scores[round_winner] += round_score

    @staticmethod
    def handle_discard(game_state, card):
        game_state.discard_card(card)
        if not any(game_state.legal_actions.values()):  # No ending action activated
            game_state.switch_turn()