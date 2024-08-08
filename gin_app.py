# gin_app.py
import logging
import os

# Ensure Kivy log mode is set to PYTHON to disable default handlers
os.environ["KIVY_LOG_MODE"] = "PYTHON"
# Set the Kivy log level to warning to suppress info and debug logs
os.environ["KIVY_LOG_LEVEL"] = "warning"

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
from kivy.clock import Clock
from kivy.logger import Logger, LOG_LEVELS, add_kivy_handlers

# Adjust specific Kivy loggers to suppress unwanted logs
logging.getLogger('kivy').setLevel(logging.WARNING)
logging.getLogger('kivy.garden').setLevel(logging.WARNING)
logging.getLogger('kivy.graphics').setLevel(logging.WARNING)
logging.getLogger('kivy.core').setLevel(logging.WARNING)

my_logger.debug("Kivy imported successfully.")

from models.game_state import GameState
from controllers.game_controller import GameController
from views.game_view import GameView

class GinApp(App):
    def build(self):
        my_logger.debug("Inside GinApp build method.")
        self.game_state = GameState()
        self.game_view = GameView(game_state=self.game_state)
        self.game_controller = GameController(game_state=self.game_state, game_view=self.game_view)
        
        self.game_view.set_controller(self.game_controller)  # Set the controller in the view
        self.game_state.add_observer(self.game_view)  # Add view as observer to the game state

        # Schedule the app to stop after 20 seconds for testing purposes
        Clock.schedule_once(self.stop_app, 40)
        
        return self.game_view

    def stop_app(self, dt):
        my_logger.debug("[GinApp] Stopping GinApp as scheduled.")
        self.stop()

if __name__ == '__main__':
    GinApp().run()
    my_logger.debug("GinApp run completed.")