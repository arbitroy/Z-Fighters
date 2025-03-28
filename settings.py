"""
Game constants and settings
"""
import pygame

# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 60
GRAVITY = 0.5
GROUND_LEVEL = HEIGHT - 100  # Ground position

# Game states
MENU = 0
GAMEPLAY = 1
PAUSE = 2
GAMEOVER = 3
CONTROLS = 4
LEVELSELECT = 5
VICTORY = 6

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (150, 75, 0)
GRAY = (150, 150, 150)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (76, 153, 0)
DIRT_BROWN = (101, 67, 33)

# Fonts
pygame.font.init()  # Initialize font system
TITLE_FONT = pygame.font.Font(None, 80)
MENU_FONT = pygame.font.Font(None, 50)
UI_FONT = pygame.font.Font(None, 36)
DEBUG_FONT = pygame.font.Font(None, 24)

# Menu options
MENU_OPTIONS = ["Play", "Level Select", "Controls", "Exit"]
LEVEL_OPTIONS = ["Level 1", "Level 2 (Locked)", "Back"]
PAUSE_OPTIONS = ["Resume", "Controls", "Quit to Menu"]
GAMEOVER_OPTIONS = ["Try Again", "Main Menu"]
VICTORY_OPTIONS = ["Next Level", "Main Menu"]

# Game difficulty settings
MAX_WAVES = 10  # Number of waves to complete for victory

# In settings.py
PLAYER_WIDTH = 40  # Set to match sprite width
PLAYER_HEIGHT = 60  # Set to match sprite height
PLAYER_SPEED = 5
PLAYER_MAX_HEALTH = 100
PLAYER_JUMP_POWER = -12  # Negative because up is negative in pygame

# Enemy settings
ZOMBIE_WIDTH = 30
ZOMBIE_HEIGHT = 50
ZOMBIE_SPEED = 2
ZOMBIE_MAX_HEALTH = 50
ZOMBIE_DAMAGE = 10
ZOMBIE_ATTACK_COOLDOWN = 30

# Projectile settings
PROJECTILE_RADIUS = 5
PROJECTILE_SPEED = 10
PROJECTILE_DAMAGE = 25
PROJECTILE_MAX_AGE = 120  # Max frames a projectile can exist

# Debug settings
DEBUG_MODE = False