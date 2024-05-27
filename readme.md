# Gin Rummy Solver (2024)

A Python project to simulate and solve Gin Rummy using Pygame.

## Directory Structure

solver/
├── assets/
│ └── card-images/
│ ├── 1C.png
│ ├── 2C.png
│ ├── ...
│ ├── back.png
├── main.py
├── game.py
├── card.py
├── deck.py
├── card_container.py
├── utils.py
├── README.md

## How to Run

1. Clone the repository.
2. Ensure you have Pygame installed (`pip install pygame`).
3. Run the game using `python main.py`.

## Game Description

This project simulates a Gin Rummy game. The main game logic is contained in `game.py`, with card and deck handling in `card.py` and `deck.py`, respectively.

## File Descriptions

- `main.py`: Entry point of the application.
- `game.py`: Contains the `Game` class and main game logic.
- `card.py`: Contains the `Card` class for card operations.
- `deck.py`: Contains the `Deck` class for deck operations.
- `card_container.py`: Contains the `CardContainer` class for managing collections of cards.
- `utils.py`: Contains utility constants and functions.