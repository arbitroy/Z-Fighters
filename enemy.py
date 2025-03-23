import pygame
import random
import math
from settings import (
    ZOMBIE_WIDTH, ZOMBIE_HEIGHT, ZOMBIE_SPEED, ZOMBIE_MAX_HEALTH,
    ZOMBIE_DAMAGE, ZOMBIE_ATTACK_COOLDOWN, BROWN, RED, GRAVITY,
    GROUND_LEVEL, WIDTH
)
from debug import add_debug

class Zombie:
    """Basic zombie enemy that moves toward the player"""
    
    def __init__(self, x, y):
        self.x = x  # World x position
        self.y = y
        self.width = ZOMBIE_WIDTH
        self.height = ZOMBIE_HEIGHT
        self.speed = ZOMBIE_SPEED
        self.health = ZOMBIE_MAX_HEALTH
        self.max_health = ZOMBIE_MAX_HEALTH
        self.damage = ZOMBIE_DAMAGE
        self.attack_cooldown = 0
        self.attack_cooldown_max = ZOMBIE_ATTACK_COOLDOWN
        self.color = BROWN
        self.velocity_y = 0
        self.on_ground = False
    
    def update(self, player_world_x, platforms):
        """Update zombie position and state"""
        # Move toward player (only horizontally in a side-scroller)
        if self.x < player_world_x:
            self.x += self.speed
        else:
            self.x -= self.speed
        
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Check platform collisions
        self.on_ground = False
        for platform in platforms:
            if platform.check_collision(self.x, self.y, self.width, self.height):
                if self.velocity_y > 0:  # Only when falling
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.on_ground = True
        
        # Check if on ground
        if self.y >= GROUND_LEVEL - self.height:
            self.y = GROUND_LEVEL - self.height
            self.velocity_y = 0
            self.on_ground = True
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def check_collision_with_player(self, player_x, player_y, player_width, player_height, camera_offset_x):
        """Check if zombie collides with the player"""
        # Calculate screen position of zombie
        screen_x = self.x - camera_offset_x
        
        # Calculate overlap between zombie and player
        overlap_x = (screen_x < player_x + player_width and 
                    screen_x + self.width > player_x)
        overlap_y = (self.y < player_y + player_height and 
                    self.y + self.height > player_y)
        
        # Return true if overlapping in both axes
        return overlap_x and overlap_y
    
    def attack_player(self, player):
        """Attack the player if cooldown allows"""
        if self.attack_cooldown <= 0:
            player.take_damage(self.damage)
            self.attack_cooldown = self.attack_cooldown_max
            add_debug(f"Player hit! Health: {player.health}")
            return True
        return False
    
    def take_damage(self, amount):
        """Reduce zombie health by the given amount"""
        self.health -= amount
        
        # Flash the zombie red briefly
        self.color = RED
        # Reset color would normally use a timer, but for simplicity we'll do it next frame
    
    def draw(self, screen, camera_offset_x, debug_mode=False):
        """Draw the zombie on the screen"""
        # Reset color to normal if it was damaged
        if self.color == RED:
            self.color = BROWN
            
        # Calculate screen position
        screen_x = self.x - camera_offset_x
        
        # Only draw if on screen (with a margin)
        if -self.width < screen_x < WIDTH + self.width:
            # Draw zombie body with camera offset
            pygame.draw.rect(screen, self.color, (screen_x, self.y, self.width, self.height))
            
            # Draw health bar above zombie
            health_bar_width = self.width
            health_bar_height = 5
            health_percentage = max(0, self.health / self.max_health)
            health_width = int(health_bar_width * health_percentage)
            
            # Health bar background
            pygame.draw.rect(
                screen,
                (100, 100, 100),
                (screen_x, self.y - 10, health_bar_width, health_bar_height)
            )
            
            # Health bar
            pygame.draw.rect(
                screen,
                RED,
                (screen_x, self.y - 10, health_width, health_bar_height)
            )
            
            # Debug: Draw collision box
            if debug_mode:
                pygame.draw.rect(screen, (255, 0, 255), 
                                (screen_x, self.y, self.width, self.height), 1)  # Draw outline

def spawn_wave(player_x, camera_offset_x, wave_size):
    """Spawn a wave of zombies around the player"""
    enemies = []
    
    # Spawn positions relative to player (world coordinates)
    spawn_positions = [
        (player_x + camera_offset_x + WIDTH, GROUND_LEVEL - 50),
        (player_x + camera_offset_x + WIDTH + 200, GROUND_LEVEL - 50),
        (player_x + camera_offset_x + WIDTH + 400, GROUND_LEVEL - 50),
        (player_x + camera_offset_x - WIDTH, GROUND_LEVEL - 50),
        (player_x + camera_offset_x - WIDTH - 200, GROUND_LEVEL - 50)
    ]
    
    for _ in range(wave_size):
        pos = random.choice(spawn_positions)
        enemies.append(Zombie(pos[0], pos[1]))
    
    add_debug(f"Spawned {wave_size} zombies")
    return enemies