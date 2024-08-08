class EndingConditions:
    @staticmethod
    def get_highest_order_action(hand, knock_card):
        if EndingConditions.can_gin(hand) == "big_gin":
            return "big_gin"
        elif EndingConditions.can_gin(hand) == "gin":
            return "gin"
        elif EndingConditions.can_knock(hand, knock_card):
            return "knock"
        return None

    @staticmethod
    def can_gin(hand):
        deadwood = hand.get_deadwood()
        if len(deadwood) == 0:
            return "big_gin"
        elif len(deadwood) == 1:
            return "gin"
        return None

    @staticmethod
    def can_knock(hand, knock_card):
        if knock_card.rank == 1:  # Ace is not a valid knock card
            return False
        deadwood_value = sum(card.calculate_rank_value() for card in hand.get_deadwood())
        highest_deadwood_value = max(card.calculate_rank_value() for card in hand.get_deadwood())
        return deadwood_value - highest_deadwood_value <= knock_card.calculate_rank_value()