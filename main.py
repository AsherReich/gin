import pygame
import time
from models.game_state import GameState
from controllers.game_controller import GameController
from views.game_view import GameView

def main():
    pygame.init()

    game_state = GameState()
    game_view = GameView()
    game_controller = GameController(game_state, game_view)

    running = True
    clock = pygame.time.Clock()
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_controller.handle_click(event.pos)

        game_controller.update_view()
        clock.tick(60)

        if time.time() - start_time > 20:  # Auto shutdown after 20 seconds
            running = False

    pygame.quit()

if __name__ == '__main__':
    main()