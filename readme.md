# Zombie Fighters

A simple 2D zombie shooting game built with Pygame.

## Project Structure

- `main.py` - The main entry point for the game
- `game_states.py` - Manages different game states (menu, gameplay, etc.)
- `player.py` - Player character with movement and shooting mechanics
- `projectile.py` - Projectiles fired by the player
- `enemy.py` - Zombie enemy classes
- `level.py` - Level design and platforms
- `menu.py` - Menu system (can be run standalone or as part of main.py)

## Controls

- **W/A/S/D** - Move player (up, left, down, right)
- **Space** - Jump
- **Left Mouse Button** - Shoot
- **ESC** - Pause game / Return to previous menu

## Game Features

- State management system for menus, gameplay, pause, and game over
- Enhanced menu with level selection
- Player movement, jumping, and shooting mechanics
- Zombie enemies that follow the player
- Wave-based enemy spawning
- Health, scoring, and wave counter systems
- Basic collision detection
- Simple placeholder graphics (rectangles and circles)

## How to Run

1. Ensure you have Python and Pygame installed
2. Run the game with: `python main.py`
3. Alternatively, you can run just the menu with: `python menu.py`

## Development Roadmap

This project is following the development plan outlined in "Zombie Fighters - Development Plan.txt".

Current status:
- [x] Project Setup and Framework
- [x] Menu System Enhancement
- [x] Core Player Mechanics
- [x] Basic Enemy System
- [x] Simple Level Design
- [x] Game Systems (health, score, waves)
- [x] Basic UI Elements
- [x] State Integration
- [ ] Visual Enhancements (placeholders used for now)
- [ ] Testing and Refinement
- [x] Documentation

## Next Steps

The next phase of development should focus on:
1. Replacing placeholder graphics with sprites
2. Adding animations
3. Enhancing level design
4. Balancing difficulty
5. Adding sound effects and music
6. Testing and fixing bugs

## Requirements

- Python 3.x
- Pygame library
