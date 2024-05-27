import pygame
import os
from models.card import Card

class GameView:
    def __init__(self, screen, game_state, image_folder):
        self.screen = screen
        self.game_state = game_state
        self.image_folder = image_folder
        self.card_width = 80  # Example dimensions
        self.card_height = 112
        self.player_card_rects = []
        self.draw_pile_rect = None
        self.discard_pile_rect = None
        self.calculate_card_positions()

    def calculate_card_positions(self):
        self.player_card_rects = []
        overlap_width = self.card_width * (1 - self.game_state.player_hand.overlap_ratio)
        for index, card in enumerate(self.game_state.player_hand):
            card_rect = pygame.Rect(
                self.game_state.player_hand.x + index * overlap_width,
                self.screen.get_height() - self.card_height - VERTICAL_MARGIN,
                overlap_width,
                self.card_height
            )
            self.player_card_rects.append((card, card_rect))

        self.draw_pile_rect = pygame.Rect(
            self.game_state.draw_pile.x,
            self.game_state.draw_pile.y,
            self.card_width,
            self.card_height
        )

        if self.game_state.discard_pile.cards:
            self.discard_pile_rect = pygame.Rect(
                self.game_state.discard_pile.x,
                self.game_state.discard_pile.y,
                self.card_width,
                self.card_height
            )
        else:
            self.discard_pile_rect = None

    def update(self, observable):
        self.game_state = observable
        self.calculate_card_positions()
        self.draw_hands()
        self.draw_piles()
        pygame.display.flip()

    def draw_hands(self):
        for card, rect in self.player_card_rects:
            image = card.load_image(self.card_width, self.card_height)
            self.screen.blit(image, rect.topleft)

    def draw_piles(self):
        draw_pile_image = pygame.image.load(f"{self.image_folder}/back.png")
        draw_pile_image = pygame.transform.scale(draw_pile_image, (self.card_width, self.card_height))
        self.screen.blit(draw_pile_image, self.draw_pile_rect.topleft)

        if self.discard_pile_rect:
            top_discard_image = self.game_state.discard_pile.cards[-1].load_image(self.card_width, self.card_height)
            self.screen.blit(top_discard_image, self.discard_pile_rect.topleft)

    def get_clicked_card(self, pos):
        for card, rect in self.player_card_rects:
            if rect.collidepoint(pos):
                return card
        return None

    def get_clicked_pile(self, pos):
        if self.draw_pile_rect and self.draw_pile_rect.collidepoint(pos):
            return 'draw_pile'
        if self.discard_pile_rect and self.discard_pile_rect.collidepoint(pos):
            return 'discard_pile'
        return None