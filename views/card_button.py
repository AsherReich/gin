from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from utils.constants import DOUBLE_CLICK_TIME

class CardButton(ButtonBehavior, Image):
    def __init__(self, card, on_click_handler=None, **kwargs):
        super().__init__(**kwargs)
        self.card = card
        self.on_click_handler = on_click_handler
        self.last_click_time = 0
        self.double_click_time = DOUBLE_CLICK_TIME  # Double click threshold
        self.bind(on_press=self.handle_press)

    def handle_press(self, instance):
        current_time = Clock.get_time()
        if current_time - self.last_click_time < self.double_click_time:
            # Double click detected
            Clock.unschedule(self.check_single_click)
            self.on_click_handler(self, 'double')
        else:
            # Schedule a check for single click after the double click threshold
            self.last_click_time = current_time
            Clock.schedule_once(self.check_single_click, self.double_click_time)

    def check_single_click(self, dt):
        # Confirm single click if no second click occurred within the threshold
        current_time = Clock.get_time()
        if current_time - self.last_click_time >= self.double_click_time:
            self.on_click_handler(self, 'single')