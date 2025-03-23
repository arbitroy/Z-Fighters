"""
Level management classes and functions
"""
import pygame
from settings import WIDTH, HEIGHT, GROUND_LEVEL, GRAY

class Platform:
    """Platform class for player to stand on"""
    
    def __init__(self, x, y, width, height, color=GRAY, is_hazard=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.is_hazard = is_hazard  # Whether this platform damages the player
    
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

class Obstacle:
    """Obstacle that blocks movement and/or damages entities"""
    
    def __init__(self, x, y, width, height, damage=10, blocks_player=True, blocks_enemies=True, blocks_projectiles=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.damage = damage
        self.blocks_player = blocks_player
        self.blocks_enemies = blocks_enemies
        self.blocks_projectiles = blocks_projectiles
        self.color = (200, 0, 0)  # Red for hazards
    
    def draw(self, screen, camera_offset_x):
        """Draw the obstacle on the screen with camera offset"""
        screen_x = self.x - camera_offset_x
        
        # Only draw if potentially visible on screen
        if screen_x + self.width > 0 and screen_x < screen.get_width():
            pygame.draw.rect(screen, self.color, (screen_x, self.y, self.width, self.height))
            
            # Draw spikes for hazards
            if self.damage > 0:
                spike_color = (255, 0, 0)
                spike_width = 10
                num_spikes = self.width // spike_width
                for i in range(int(num_spikes)):
                    spike_x = screen_x + i * spike_width
                    pygame.draw.polygon(screen, spike_color, [
                        (spike_x, self.y),
                        (spike_x + spike_width // 2, self.y - 10),
                        (spike_x + spike_width, self.y)
                    ])
    
    def check_collision(self, x, y, width, height):
        """Check if the obstacle collides with the given rectangle"""
        return (self.x < x + width and
                self.x + self.width > x and
                self.y < y + height and
                self.y + self.height > y)

def create_level(level_number):
    """Create and return platforms and obstacles for the specified level"""
    platforms = []
    obstacles = []
    
    if level_number == 1:
        # Ground platform (spans the entire level)
        ground = Platform(0, GROUND_LEVEL, WIDTH * 4, HEIGHT - GROUND_LEVEL)
        platforms.append(ground)
        
        # Add some floating platforms
        platforms.append(Platform(300, GROUND_LEVEL - 120, 200, 20))
        platforms.append(Platform(600, GROUND_LEVEL - 200, 200, 20))
        
        # Create a gap with a hazard
        obstacles.append(Obstacle(800, GROUND_LEVEL - 10, 100, 10, damage=20))
        
        # More platforms after the gap
        platforms.append(Platform(900, GROUND_LEVEL - 150, 200, 20))
        
        # Elevated section with obstacles underneath
        platforms.append(Platform(1200, GROUND_LEVEL - 250, 300, 20))
        obstacles.append(Obstacle(1250, GROUND_LEVEL - 50, 200, 10, damage=15))
        
        # Create a challenging area
        platforms.append(Platform(1600, GROUND_LEVEL - 180, 100, 20))
        platforms.append(Platform(1800, GROUND_LEVEL - 130, 100, 20))
        platforms.append(Platform(2000, GROUND_LEVEL - 200, 150, 20))
        
        # Wall that blocks enemies but not projectiles
        obstacles.append(Obstacle(2300, GROUND_LEVEL - 150, 20, 150, damage=0, 
                                blocks_player=True, blocks_enemies=True, blocks_projectiles=False))
        
        # Safe platform after wall
        platforms.append(Platform(2400, GROUND_LEVEL - 100, 300, 20))
        
        # Final section with challenges
        platforms.append(Platform(2800, GROUND_LEVEL - 150, 100, 20))
        obstacles.append(Obstacle(2900, GROUND_LEVEL - 10, 150, 10, damage=25))
        platforms.append(Platform(3050, GROUND_LEVEL - 180, 100, 20))
        platforms.append(Platform(3250, GROUND_LEVEL - 220, 150, 20))
    
    elif level_number == 2:
        # Ground platform (spans the entire level)
        ground = Platform(0, GROUND_LEVEL, WIDTH * 5, HEIGHT - GROUND_LEVEL)
        platforms.append(ground)
        
        # Create a more complex level with multiple paths
        
        # Lower path with hazards
        obstacles.append(Obstacle(300, GROUND_LEVEL - 15, 80, 15, damage=10))
        obstacles.append(Obstacle(600, GROUND_LEVEL - 15, 120, 15, damage=15))
        obstacles.append(Obstacle(900, GROUND_LEVEL - 15, 150, 15, damage=20))
        
        # Upper path with challenging jumps
        platforms.append(Platform(200, GROUND_LEVEL - 150, 80, 20))
        platforms.append(Platform(400, GROUND_LEVEL - 200, 80, 20))
        platforms.append(Platform(600, GROUND_LEVEL - 250, 80, 20))
        platforms.append(Platform(800, GROUND_LEVEL - 300, 120, 20))
        
        # Middle section with obstacles
        platforms.append(Platform(1000, GROUND_LEVEL - 200, 300, 20))
        obstacles.append(Obstacle(1150, GROUND_LEVEL - 240, 100, 20, damage=25))
        
        # Vertical challenge section
        for i in range(5):
            platforms.append(Platform(1400 + i*150, GROUND_LEVEL - 120 - i*40, 80, 20))
        
        # Wall that blocks enemies
        obstacles.append(Obstacle(2300, GROUND_LEVEL - 200, 30, 200, damage=0, 
                                blocks_player=True, blocks_enemies=True, blocks_projectiles=False))
        
        # Final challenging section
        platforms.append(Platform(2400, GROUND_LEVEL - 150, 100, 20))
        platforms.append(Platform(2600, GROUND_LEVEL - 200, 100, 20))
        platforms.append(Platform(2800, GROUND_LEVEL - 250, 100, 20))
        platforms.append(Platform(3000, GROUND_LEVEL - 300, 150, 20))
        obstacles.append(Obstacle(3000, GROUND_LEVEL - 50, 250, 20, damage=30))
        
        # Safe final platform
        platforms.append(Platform(3300, GROUND_LEVEL - 150, 300, 20))
    
    return platforms, obstacles

def draw_level_background(screen):
    """Draw the level background (sky, ground, etc.)"""
    # Draw sky
    screen.fill((135, 206, 235))  # Sky blue
    
    # Draw some clouds
    clouds = [
        (50, 50, 100, 40),
        (200, 80, 150, 50),
        (400, 40, 120, 30),
        (600, 90, 140, 45)
    ]
    
    for cloud in clouds:
        x, y, width, height = cloud
        # Base cloud shape
        pygame.draw.ellipse(screen, (255, 255, 255), (x, y, width, height))
        pygame.draw.ellipse(screen, (255, 255, 255), (x + width//4, y - height//2, width//2, height))
        pygame.draw.ellipse(screen, (255, 255, 255), (x + width//3, y + height//3, width//2, height//2))
    
    # Draw distant mountains
    pygame.draw.polygon(screen, (100, 100, 100), [(0, 200), (100, 120), (200, 180), (300, 100), (400, 160), (WIDTH, 200)])
    
    # Draw ground
    pygame.draw.rect(screen, (101, 67, 33), (0, GROUND_LEVEL, WIDTH, HEIGHT - GROUND_LEVEL))  # Brown ground
    pygame.draw.rect(screen, (76, 153, 0), (0, GROUND_LEVEL, WIDTH, 5))  # Green grass line