# Spaceship Battle AI

A spaceship battle game where a human-controlled spaceship fights against an AI-controlled opponent, built with Python and Pygame.

The player controls the red spaceship, while the yellow spaceship is controlled by the AI.

## Features

- Player vs AI spaceship battle
- Player-controlled red spaceship
- AI-controlled yellow spaceship
- WASD movement for the player
- Mouse left-click shooting
- Controlled player firing cooldown
- AI automatic shooting
- AI vertical movement tracking
- AI tracking dead zone
- Health system
- Bullet collision detection
- Maximum active bullet limit
- Winner screen
- Game restart option
- Keyboard shortcut to quit
- FPS-controlled game loop

## Controls

### Player

| Key / Input | Action |
|---|---|
| W | Move Up |
| A | Move Left |
| S | Move Down |
| D | Move Right |
| Left Mouse Button | Fire |
| R | Restart after game over |
| ESC | Quit the game |

## How to Play

1. Run the game.
2. Control the red spaceship using W, A, S, and D.
3. Use the left mouse button to fire bullets.
4. The yellow AI spaceship automatically tracks the player's vertical position.
5. The AI automatically fires bullets.
6. Avoid incoming attacks and reduce the opponent's health.
7. The first side whose health reaches zero loses.
8. Press R after the match to start a new game.
9. Press ESC to quit.

## Requirements

- Python 3.8 or later
- Pygame 2.6.1

## Installation

Clone the repository:

git clone https://github.com/RaavanHrishi07/Spaceship-Battle-AI.git

Move into the project directory:

cd Spaceship-Battle-AI

Install the required dependency:

pip install -r requirements.txt

## Run the Game

python main.py

## Gameplay Details

- Both spaceships start with 10 health points.
- The player can have a maximum of 3 active bullets.
- The AI can also have a maximum of 3 active bullets.
- Player shots have a controlled firing cooldown.
- The AI follows the player's vertical position while maintaining a small tracking dead zone.
- A successful bullet collision reduces the opponent's health by 1.

## Project Structure

Spaceship-Battle-AI/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE

## Technologies Used

- Python
- Pygame

## Author

Hrishikesh Sharma

GitHub: RaavanHrishi07

## License

This project is licensed under the MIT License. See the LICENSE file for details.