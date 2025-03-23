import pygame
import math
from settings import (
    PROJECTILE_RADIUS, PROJECTILE_SPEED, PROJECTILE_DAMAGE, 
    PROJECTILE_MAX_AGE, YELLOW
)

class Projectile:
    """Projectile class for player's bullets"""
    
    def __init__(self, x, y, dir_x, dir_y):
        self.x = x  # World x position
        self.y = y
        self.radius = PROJECTILE_RADIUS
        self.speed = PROJECTILE_SPEED
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.damage = PROJECTILE_DAMAGE
        self.color = YELLOW
        self.age = 0  # Track how long the projectile has existed
        self.max_age = PROJECTILE_MAX_AGE  # Maximum frames the projectile can exist
    
    def update(self):
        """Update projectile position and age"""
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        self.age += 1
    
    def check_collision(self, enemy):
        """Check if projectile collides with an enemy"""
        # Calculate distance between projectile and enemy center
        enemy_center_x = enemy.x + enemy.width / 2
        enemy_center_y = enemy.y + enemy.height / 2
        
        # Simple distance-based collision
        dx = self.x - enemy_center_x
        dy = self.y - enemy_center_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # For better precision, use a smaller collision radius for enemy
        return distance < self.radius + min(enemy.width, enemy.height) / 3
    
    def is_offscreen(self, camera_offset_x, screen_width, screen_height):
        """Check if projectile is off-screen or too old"""
        return (self.age > self.max_age or
                self.x < camera_offset_x - 100 or 
                self.x > camera_offset_x + screen_width + 100 or 
                self.y < -100 or 
                self.y > screen_height + 100)
    
    def draw(self, screen, camera_offset_x, debug_mode=False):
        """Draw the projectile on the screen"""
        # Calculate screen position with camera offset
        screen_x = self.x - camera_offset_x
        
        # Draw projectile
        pygame.draw.circle(screen, self.color, (int(screen_x), int(self.y)), self.radius)
        
        # Debug: Draw collision circle
        if debug_mode:
            pygame.draw.circle(screen, (255, 0, 255), (int(screen_x), int(self.y)), 
                              self.radius, 1)  # Draw outline