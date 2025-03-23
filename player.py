import pygame
import math
from settings import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_MAX_HEALTH, 
    PLAYER_JUMP_POWER, GREEN, WIDTH, GRAVITY, GROUND_LEVEL
)
from projectile import Projectile
from debug import add_debug

class Player:
    """
    Player class with movement, shooting, and health mechanics
    """
    def __init__(self, x, y):
        # Position and dimensions
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        
        # Health
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        
        # Movement state
        self.moving_left = False
        self.moving_right = False
        self.velocity_y = 0
        self.on_ground = True
        
        # Visuals
        self.color = GREEN
    
    def move(self, platforms, camera_offset_x):
        """Update player position and handle collisions"""
        # Track if the player moved
        player_moved = False
        
        # Horizontal movement
        if self.moving_left:
            self.x -= self.speed
            player_moved = True
        if self.moving_right:
            self.x += self.speed
            player_moved = True
        
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Check platform collisions
        self.on_ground = False
        world_x = self.x + camera_offset_x  # Calculate world position
        
        for platform in platforms:
            if platform.check_collision(world_x, self.y, self.width, self.height):
                if self.velocity_y > 0:  # Only when falling
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.on_ground = True
        
        # Check if player is on ground
        if self.y >= GROUND_LEVEL - self.height:
            self.y = GROUND_LEVEL - self.height
            self.velocity_y = 0
            self.on_ground = True
        
        # Keep player within left boundary
        if self.x < 0:
            self.x = 0
    
    def jump(self):
        """Make the player jump"""
        if self.on_ground:
            self.velocity_y = PLAYER_JUMP_POWER
            self.on_ground = False
            add_debug("Player jumped")
    
    def shoot(self, mouse_pos, camera_offset_x, projectiles):
        """Create a projectile in the direction of the mouse cursor"""
        # Get mouse position
        mouse_x, mouse_y = mouse_pos
        
        # Convert player screen position to world position
        player_world_pos_x = self.x + camera_offset_x
        
        # Calculate direction vector
        dir_x = (mouse_x + camera_offset_x) - (player_world_pos_x + self.width/2)
        dir_y = mouse_y - (self.y + self.height/2)
        
        # Normalize the direction vector
        length = math.sqrt(dir_x ** 2 + dir_y ** 2)
        if length > 0:
            dir_x /= length
            dir_y /= length
        
        # Create projectile at player's world position
        projectile = Projectile(
            player_world_pos_x + self.width // 2,
            self.y + self.height // 2,
            dir_x, dir_y
        )
        
        # Add projectile to the game's projectiles list
        projectiles.append(projectile)
        add_debug(f"Projectile created at ({projectile.x:.1f}, {projectile.y:.1f})")
    
    def take_damage(self, amount):
        """Reduce player health by the given amount"""
        self.health -= amount
        self.color = (255, 0, 0)  # Flash red
        # Will be reset to green on next draw
    
    def draw(self, screen, debug_mode=False):
        """Draw the player on the screen"""
        # Reset color to normal
        self.color = GREEN
        
        # Draw player body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw debug info
        if debug_mode:
            # Draw collision box
            pygame.draw.rect(screen, (255, 0, 255), 
                            (self.x, self.y, self.width, self.height), 1)