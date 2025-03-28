"""
Parallax background system for Zombie Fighters
"""
import pygame
import os
from settings import WIDTH, HEIGHT

class ParallaxLayer:
    """A single layer in the parallax background system"""
    
    def __init__(self, image_path, scale=1.0, scroll_speed=1.0):
        """
        Initialize a parallax layer
        
        Args:
            image_path (str): Path to the image file
            scale (float): Scale factor for the image (default: 1.0)
            scroll_speed (float): Speed multiplier for parallax effect (default: 1.0)
                                 Values < 1 move slower than the camera (background)
                                 Values > 1 move faster than the camera (foreground)
        """
        self.scroll_speed = scroll_speed
        self.offset = 0
        
        # Load image
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
            
            # Scale image if needed
            if scale != 1.0:
                new_width = int(self.original_image.get_width() * scale)
                new_height = int(self.original_image.get_height() * scale)
                self.original_image = pygame.transform.scale(self.original_image, (new_width, new_height))
                
            # Store image dimensions
            self.width = self.original_image.get_width()
            self.height = self.original_image.get_height()
            
            # Create the image for rendering
            self.image = self.original_image
            
            # If image is smaller than screen width, create a wider image by repeating
            if self.width < WIDTH * 2:
                # Create a surface wide enough to cover screen with scrolling
                repeats = (WIDTH * 2) // self.width + 1
                self.image = pygame.Surface((self.width * repeats, self.height), pygame.SRCALPHA)
                
                # Fill with repeated copies of the original image
                for i in range(repeats):
                    self.image.blit(self.original_image, (i * self.width, 0))
                    
                # Update width to new width
                self.width = self.image.get_width()
                
        except pygame.error as e:
            print(f"Error loading parallax image '{image_path}': {e}")
            # Create a placeholder surface
            self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            self.width = WIDTH
            self.height = HEIGHT
    
    def update(self, camera_offset_x):
        """
        Update the layer offset based on camera position
        
        Args:
            camera_offset_x (float): The camera's x offset in the world
        """
        # Calculate offset based on camera position and scroll speed
        self.offset = -(camera_offset_x * self.scroll_speed) % self.width
    
    def draw(self, screen, y_pos=0):
        """
        Draw the layer to the screen
        
        Args:
            screen (pygame.Surface): The screen to draw on
            y_pos (int): Y position to draw the layer (default: 0)
        """
        # Draw the image and its wrap-around if needed
        screen.blit(self.image, (self.offset, y_pos))
        
        # If the offset creates a gap on the right side, draw the image again
        if self.offset + self.width < WIDTH:
            screen.blit(self.image, (self.offset + self.width, y_pos))

class ParallaxBackground:
    """Manager for multiple parallax background layers"""
    
    def __init__(self):
        """Initialize the parallax background system"""
        self.layers = []
        
    def add_layer(self, image_path, scale=1.0, scroll_speed=1.0):
        """
        Add a new parallax layer
        
        Args:
            image_path (str): Path to the image file
            scale (float): Scale factor for the image
            scroll_speed (float): Speed multiplier for parallax effect
        """
        layer = ParallaxLayer(image_path, scale, scroll_speed)
        self.layers.append(layer)
        return layer
    
    def update(self, camera_offset_x):
        """
        Update all parallax layers
        
        Args:
            camera_offset_x (float): The camera's x offset in the world
        """
        for layer in self.layers:
            layer.update(camera_offset_x)
    
    def draw(self, screen):
        """
        Draw all parallax layers to the screen
        
        Args:
            screen (pygame.Surface): The screen to draw on
        """
        for i, layer in enumerate(self.layers):
            # Calculate vertical position based on layer index
            # This is a simple implementation - you might want to customize this
            y_pos = 0
            
            # Draw the layer
            layer.draw(screen, y_pos)

def create_parallax_background():
    """
    Create and return a configured parallax background
    
    Returns:
        ParallaxBackground: A configured parallax background with layers
    """
    parallax = ParallaxBackground()
    
    # Define asset paths
    asset_paths = {
        'sky1': 'assetpack sky1.png',
        'sky2': 'assetpack sky2.png',
        'bg3': 'assetpack bg3.png',    # Farthest city
        'bg2': 'assetpack bg2.png',    # Middle city
        'bg1': 'assetpack bg1.png',    # Closest city
        'smog': 'assetpack smog large.png'
    }
    
    # Check which assets exist and add them
    
    # Sky (slowest moving - farthest back)
    if os.path.exists(asset_paths['sky1']):
        parallax.add_layer(asset_paths['sky1'], scale=1.0, scroll_speed=0.0)
    elif os.path.exists(asset_paths['sky2']):
        parallax.add_layer(asset_paths['sky2'], scale=1.0, scroll_speed=0.0)
    
    # Background city silhouettes
    if os.path.exists(asset_paths['bg3']):
        parallax.add_layer(asset_paths['bg3'], scale=1.0, scroll_speed=0.1)
    
    if os.path.exists(asset_paths['bg2']):
        parallax.add_layer(asset_paths['bg2'], scale=1.0, scroll_speed=0.2)
    
    if os.path.exists(asset_paths['bg1']):
        parallax.add_layer(asset_paths['bg1'], scale=1.0, scroll_speed=0.3)
    
    # Atmospheric effects (smog, fog, etc.)
    if os.path.exists(asset_paths['smog']):
        parallax.add_layer(asset_paths['smog'], scale=1.0, scroll_speed=0.4)
    
    return parallax