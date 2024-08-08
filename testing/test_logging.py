# test_logging.py
import logging
import os

# Ensure Kivy log mode is set to PYTHON to disable default handlers
os.environ["KIVY_LOG_MODE"] = "PYTHON"

# Configure custom logger
my_logger = logging.getLogger('my_app')
my_logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
my_logger.addHandler(console_handler)

my_logger.debug("Logging is configured correctly for my_app.")

# Import Kivy and configure its logging
from kivy.app import App
from kivy.logger import Logger, LOG_LEVELS, add_kivy_handlers

# Optionally add Kivy handlers if needed
# add_kivy_handlers(my_logger)

my_logger.debug("Kivy imported successfully.")

class GameState:
    def __init__(self):
        my_logger.debug("GameState initialized.")

class TestApp(App):
    def build(self):
        my_logger.debug("Inside TestApp build method.")
        self.game_state = GameState()
        return None

if __name__ == '__main__':
    TestApp().run()
    my_logger.debug("TestApp run completed.")