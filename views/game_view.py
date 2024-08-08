import os
import logging
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.animation import Animation
from kivy.graphics import Color, Line
from views.card_button import CardButton
from utils.constants import (
    CARD_WIDTH_RATIO,
    CARD_HEIGHT_RATIO,
    IMAGE_FOLDER,
    HORIZONTAL_MARGIN,
    VERTICAL_MARGIN,
    PILE_OFFSET_X,
    PILES_Y_POSITION
)


class CircularButton(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super(CircularButton, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        with self.canvas.before:
            self.border_color = (1, 1, 1, 1)  # White border
            self.border_width = 2

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.border_color)
            Line(ellipse=(self.x, self.y, self.width, self.height), width=self.border_width)


class GameView(FloatLayout, EventDispatcher):
    def __init__(self, game_state, **kwargs):
        super().__init__(**kwargs)
        self.game_state = game_state
        self.card_width = int(Window.width * CARD_WIDTH_RATIO)
        self.card_height = int(self.card_width * CARD_HEIGHT_RATIO)
        self.card_images = self.load_card_images()
        self.action_button = self.create_action_button()  # Create but don't add the action button yet
        self.update_view()

        # Register custom events
        self.register_event_type('on_draw_pile_click')
        self.register_event_type('on_discard_pile_click')
        self.register_event_type('on_card_single_click')
        self.register_event_type('on_card_double_click')
        self.register_event_type('on_action_button_click')

    def set_controller(self, controller):
        self.controller = controller

    def load_card_images(self):
        card_images = {}
        for rank in range(1, 14):
            for suit in "cdhs":
                card_name = f"{rank}{suit}"
                image_path = os.path.join(IMAGE_FOLDER, f"{card_name}.png")
                card_images[card_name] = image_path
        card_images['back'] = os.path.join(IMAGE_FOLDER, "back.png")
        return card_images

    def create_action_button(self):
        action_button = CircularButton(
            text='Action',
            size_hint=(None, None),
            size=(self.card_width, self.card_width),  # Make the button circular
            color=(1, 1, 1, 1),
            font_size=20,
            halign='center',
            valign='middle'
        )
        action_button.bind(on_press=self.handle_action_button_click)
        return action_button

    def handle_action_button_click(self, instance):
        if instance.text in ['Gin', 'Big Gin', 'Knock']:
            self.dispatch('on_action_button_click', instance.text)

    def handle_click(self, instance, click_type):
        if instance == self.draw_pile_button:
            self.dispatch('on_draw_pile_click')
        elif instance == self.discard_pile_button:
            self.dispatch('on_discard_pile_click')
        elif instance in [btn for btn in self.children if isinstance(btn, CardButton) and btn.card in self.game_state.get_player_hand().cards]:
            if click_type == 'single':
                self.dispatch('on_card_single_click', instance.card)
            elif click_type == 'double':
                self.dispatch('on_card_double_click', instance.card)
        else:
            logging.warning("Unknown click event")

    def update_view(self, *args):
        logging.debug("[GameView] Update view called")
        self.clear_widgets()
        self.display_piles()
        self.display_player_hand()
        self.display_opponent_hand()
        self.update_action_button()  # Update and add the action button

    def display_player_hand(self):
        hand = self.game_state.get_player_hand()
        #logging.debug(f"Player hand: {hand.cards}")

        melds = hand.get_melds()
        deadwood = hand.get_deadwood()
        #logging.debug(f"Melds: {melds}, Deadwood: {deadwood}")

        start_x = HORIZONTAL_MARGIN
        overlap_width = self.card_width * 0.7

        # Display deadwood cards
        for index, card in enumerate(deadwood):
            card_rect = (start_x + index * overlap_width, VERTICAL_MARGIN)
            card_button = CardButton(
                card=card,
                on_click_handler=self.handle_click,
                source=self.card_images[f"{card.rank}{card.suit.lower()}"],
                size_hint=(None, None),
                size=(self.card_width, self.card_height),
                pos=card_rect
            )
            self.add_widget(card_button)

        # Display meld cards
        meld_y = VERTICAL_MARGIN + self.card_height * 0.25
        meld_x = start_x + len(deadwood) * overlap_width

        for meld in melds:
            for card in meld:
                card_button = CardButton(
                    card=card,
                    on_click_handler=self.handle_click,
                    source=self.card_images[f"{card.rank}{card.suit.lower()}"],
                    size_hint=(None, None),
                    size=(self.card_width * 0.8, self.card_height * 0.8),
                    pos=(meld_x, meld_y)
                )
                self.add_widget(card_button)
                meld_x += overlap_width * 0.8
            meld_x += 20

    def update_action_button(self):
        new_x_pos = HORIZONTAL_MARGIN - self.card_width
        new_y_pos = VERTICAL_MARGIN + (self.card_height - self.card_width) / 2

        logging.debug(f"[GameView] Action button position: {(new_x_pos, new_y_pos)}")
        self.action_button.pos = (new_x_pos, new_y_pos)
        
        legal_actions = self.game_state.legal_actions
        if legal_actions["big_gin"]:
            self.action_button.text = "Big Gin"
            self.action_button.background_color = (0, 1, 0, 1)
            self.flash_action_button()
            #logging.debug("[GameView] Action button set to Big Gin")
        elif legal_actions["gin"]:
            self.action_button.text = "Gin"
            self.action_button.background_color = (0, 1, 0, 1)
            self.flash_action_button()
            #logging.debug("[GameView] Action button set to Gin")
        elif legal_actions["knock"]:
            self.action_button.text = "Knock"
            self.action_button.background_color = (0, 1, 0, 1)
            self.flash_action_button()
            #logging.debug("[GameView] Action button set to Knock")
        else:
            self.action_button.text = "Action"
            self.action_button.background_color = (0, 0, 0, 1)
            #logging.debug("[GameView] Action button set to default Action")

        if self.action_button not in self.children:
            self.add_widget(self.action_button)
            #logging.debug("[GameView] Action button added to widget tree")

    def flash_action_button(self):
        animation = Animation(color=(1, 1, 1, 1), duration=0.5) + Animation(color=(0, 1, 0, 1), duration=0.5)
        animation.repeat = True
        animation.start(self.action_button)

    def display_opponent_hand(self):
        hand = self.game_state.get_opponent_hand()
        #logging.debug(f"Opponent hand: {hand.cards}")
        opponent_hand_length = len(hand.cards)
        start_x = HORIZONTAL_MARGIN
        overlap_width = self.card_width * 0.7

        for index in range(opponent_hand_length):
            card_rect = (start_x + index * overlap_width, Window.height - self.card_height - VERTICAL_MARGIN)
            card_image = Image(
                source=self.card_images['back'],
                size_hint=(None, None),
                size=(self.card_width, self.card_height),
                pos=card_rect
            )
            self.add_widget(card_image)

    def display_piles(self):
        pile_y_position = Window.height * PILES_Y_POSITION
        center_x = Window.width // 2

        draw_pile_x = center_x - self.card_width - PILE_OFFSET_X
        discard_pile_x = center_x + PILE_OFFSET_X

        draw_pile_rect = (draw_pile_x, pile_y_position - self.card_height / 2)
        self.draw_pile_button = CardButton(
            card=None,
            on_click_handler=self.handle_click,
            source=self.card_images['back'],
            size_hint=(None, None),
            size=(self.card_width, self.card_height),
            pos=draw_pile_rect
        )
        self.add_widget(self.draw_pile_button)

        if self.game_state.get_discard_pile():
            discard_pile_rect = (discard_pile_x, pile_y_position - self.card_height / 2)
            top_discard_card = self.game_state.get_discard_pile()[-1]
            self.discard_pile_button = CardButton(
                card=top_discard_card,
                on_click_handler=self.handle_click,
                source=self.card_images[f"{top_discard_card.rank}{top_discard_card.suit.lower()}"],
                size_hint=(None, None),
                size=(self.card_width, self.card_height),
                pos=discard_pile_rect
            )
            self.add_widget(self.discard_pile_button)

    def animate_sort_and_meld(self, sorted_hand, melds, deadwood):
        logging.debug(f"Animating sort and meld: sorted_hand={sorted_hand}, melds={melds}, deadwood={deadwood}")
        start_x = HORIZONTAL_MARGIN
        num_cards = len(sorted_hand)
        overlap_width = self.card_width * 0.7  # Constant overlap width

        # First, position all cards as unsorted
        for index, card in enumerate(self.game_state.get_player_hand().cards):
            card_button = self.get_card_button(card)
            card_button.pos = (start_x + index * overlap_width, VERTICAL_MARGIN)
            self.add_widget(card_button)

        # Animate sorting and melding
        for index, card in enumerate(sorted_hand):
            card_button = self.get_card_button(card)
            new_x = start_x + index * overlap_width
            anim = Animation(pos=(new_x, VERTICAL_MARGIN), duration=0.5)
            anim.start(card_button)

        # Separate melds to a different corner
        meld_y = VERTICAL_MARGIN + self.card_height * 0.25  # Slightly jutted up
        meld_index = 0
        for meld in melds:
            meld_x = start_x + num_cards * overlap_width + meld_index * (self.card_width * 0.8 + 20)  # Add space between melds
            for card in meld:
                card_button = self.get_card_button(card)
                anim = Animation(pos=(meld_x, meld_y), size=(self.card_width * 0.8, self.card_height * 0.8), duration=0.5)
                anim.start(card_button)
                meld_x += overlap_width * 0.8  # Adjust for scaled down size
            meld_index += 1

    def get_card_button(self, card):
        for child in self.children:
            if isinstance(child, CardButton) and child.card == card:
                return child
        return None

    def update_legal_actions(self, legal_actions):
        self.legal_actions = legal_actions
        self.update_action_button()

    # Default event handlers
    def on_draw_pile_click(self, *args):
        pass

    def on_discard_pile_click(self, *args):
        pass

    def on_card_single_click(self, *args):
        pass

    def on_card_double_click(self, *args):
        pass

    def on_action_button_click(self, *args):
        pass