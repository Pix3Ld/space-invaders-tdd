# Space Invaders

This project is a simple 2D arcade shooter inspired by classic Space Invaders. The game is built in Python with Pygame and includes enemy waves, player movement, shooting, collision handling, score tracking, barriers, and basic sound effects.

## Features

- Player-controlled spaceship movement
- Shooting mechanics with cooldown
- Enemy waves with directional movement
- Collision detection for bullets and barriers
- Score and high score saving to `highscore.txt`
- Audio and sprite asset support
- Unit tests for game logic and assets

## Project structure

- `main.py` – application entry point
- `game/` – game logic, entities, renderer, and asset manager
- `assets/` – images and sounds used by the game
- `tests/` – pytest-based tests
- `requirements.txt` – Python dependencies
- `highscore.txt` – saved high score

## Requirements

Python 3.10+ is recommended.

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the game

From the project root:

```bash
python main.py
```

## Controls

- Left arrow: move left
- Right arrow: move right
- Space: shoot
- Escape: exit the game
- R: restart after game over

## Gameplay

- Protect your ship from incoming enemy projectiles.
- Eliminate the alien formation before it reaches the bottom of the screen.
- Use the barriers to absorb damage and survive longer.
- Try to beat your high score.

## Testing

Run the test suite with:

```bash
pytest
```

This project includes tests covering game entities, game flow, and asset loading behavior.

## Notes

The project includes fallback asset generation for images and audio when no files are found in the `assets` folders, which makes it easier to run in clean environments.
