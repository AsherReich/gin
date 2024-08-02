class CardContainer:
    def __init__(self, x, y, horizontal=True, overlap_ratio=0.3):
        self.x = x
        self.y = y
        self.horizontal = horizontal
        self.overlap_ratio = overlap_ratio
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def clear(self):
        self.cards = []

    def get_card_positions(self, card_width, card_height):
        positions = []
        offset = 0
        for index, card in enumerate(self.cards):
            if self.horizontal:
                pos_x = self.x + offset
                pos_y = self.y
                offset += card_width * (1 - self.overlap_ratio)
            else:
                pos_x = self.x
                pos_y = self.y + offset
                offset += card_height * (1 - self.overlap_ratio)
            positions.append((pos_x, pos_y))
        return positions
