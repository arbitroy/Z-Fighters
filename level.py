import pygame
from settings import WIDTH, HEIGHT, GROUND_LEVEL, GRAY

class Platform:
    """Platform class for player to stand on"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = GRAY
    
    def draw(self, screen, camera_offset_x):
        """Draw the platform on the screen with camera offset"""
        screen_x = self.x - camera_offset_x
        pygame.draw.rect(screen, self.color, (screen_x, self.y, self.width, self.height))
    
    def check_collision(self, x, y, width, height):
        """Check if the platform collides with the given rectangle"""
        return (self.x < x + width and
                self.x + self.width > x and
                self.y < y + height and
                self.y + self.height > y)

def create_level(level_number):
    """Create and return platforms for the specified level"""
    platforms = []
    
    if level_number == 1:
        # Ground platform (spans the entire level)
        ground = Platform(0, GROUND_LEVEL, WIDTH * 3, HEIGHT - GROUND_LEVEL)
        platforms.append(ground)
        
        # Add some floating platforms
        platforms.append(Platform(300, GROUND_LEVEL - 120, 200, 20))
        platforms.append(Platform(600, GROUND_LEVEL - 200, 200, 20))
        platforms.append(Platform(900, GROUND_LEVEL - 150, 200, 20))
        platforms.append(Platform(1200, GROUND_LEVEL - 250, 200, 20))
        platforms.append(Platform(1500, GROUND_LEVEL - 180, 200, 20))
    
    elif level_number == 2:
        # Ground platform (spans the entire level)
        ground = Platform(0, GROUND_LEVEL, WIDTH * 4, HEIGHT - GROUND_LEVEL)
        platforms.append(ground)
        
        # More complex arrangement of platforms
        platforms.append(Platform(200, GROUND_LEVEL - 100, 100, 20))
        platforms.append(Platform(350, GROUND_LEVEL - 180, 100, 20))
        platforms.append(Platform(500, GROUND_LEVEL - 260, 100, 20))
        platforms.append(Platform(650, GROUND_LEVEL - 180, 100, 20))
        platforms.append(Platform(800, GROUND_LEVEL - 100, 100, 20))
        
        # Add some additional platforms
        platforms.append(Platform(1000, GROUND_LEVEL - 150, 300, 20))
        platforms.append(Platform(1400, GROUND_LEVEL - 220, 300, 20))
        platforms.append(Platform(1800, GROUND_LEVEL - 150, 300, 20))
        platforms.append(Platform(2200, GROUND_LEVEL - 220, 300, 20))
    
    return platforms

def draw_level_background(screen):
    """Draw the level background (sky, ground, etc.)"""
    # Draw sky
    screen.fill((135, 206, 235))  # Sky blue
    
    # Draw ground
    pygame.draw.rect(screen, (101, 67, 33), (0, GROUND_LEVEL, WIDTH, HEIGHT - GROUND_LEVEL))  # Brown ground
    pygame.draw.rect(screen, (76, 153, 0), (0, GROUND_LEVEL, WIDTH, 5))  # Green grass line