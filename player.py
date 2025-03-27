import pygame
import math
import os
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
        self.facing_right = True
        
        # Animation
        self.animation_state = "idle"  # idle or walking
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_delay = 8  # Frames between sprite changes
        
        # Debug info
        add_debug("Player: Initializing sprite system")
        
        # Load sprites
        self.use_sprites = True  # Set to False to completely disable sprite rendering
        self.sprites = self.load_sprites()
        
        # Visuals (fallback color)
        self.color = GREEN
        
        # Damage flash effect
        self.is_hit = False
        self.hit_timer = 0
        
        add_debug("Player: Initialization complete")
    
    def load_sprites(self):
        """Load all player sprite images"""
        add_debug("Player: Loading sprites...")
        
        sprites = {
            "idle": {
                "right": [],
                "left": []
            },
            "walking": {
                "right": [],
                "left": []
            }
        }
        
        # Check if we have the assets/player directory
        if not os.path.exists("assets/player"):
            add_debug("Player: 'assets/player' directory not found!")
            self.create_fallback_sprites(sprites)
            return sprites
        
        # Try to load sprites from assets/player directory
        try:
            # Load idle right sprites
            for i in range(4):
                sprite_path = f"assets/player/idle_right_{i}.png"
                if os.path.exists(sprite_path):
                    # Load sprite without scaling - keep original size
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    sprites["idle"]["right"].append(sprite)
                    add_debug(f"Player: Loaded {sprite_path}, size: {sprite.get_size()}")
            
            # Load walking right sprites
            for i in range(4):
                sprite_path = f"assets/player/walking_right_{i}.png"
                if os.path.exists(sprite_path):
                    # Load sprite without scaling
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    sprites["walking"]["right"].append(sprite)
                    add_debug(f"Player: Loaded {sprite_path}, size: {sprite.get_size()}")
            
            # Check if we have left sprites or need to flip right sprites
            left_exists = os.path.exists("assets/player/idle_left_0.png")
            
            if left_exists:
                # Load idle left sprites
                for i in range(4):
                    sprite_path = f"assets/player/idle_left_{i}.png"
                    if os.path.exists(sprite_path):
                        # Load sprite without scaling
                        sprite = pygame.image.load(sprite_path).convert_alpha()
                        sprites["idle"]["left"].append(sprite)
                
                # Load walking left sprites
                for i in range(4):
                    sprite_path = f"assets/player/walking_left_{i}.png"
                    if os.path.exists(sprite_path):
                        # Load sprite without scaling
                        sprite = pygame.image.load(sprite_path).convert_alpha()
                        sprites["walking"]["left"].append(sprite)
            else:
                # Flip right sprites for left
                for sprite in sprites["idle"]["right"]:
                    sprites["idle"]["left"].append(pygame.transform.flip(sprite, True, False))
                
                for sprite in sprites["walking"]["right"]:
                    sprites["walking"]["left"].append(pygame.transform.flip(sprite, True, False))
            
            # Verify we have all necessary sprites
            if not sprites["idle"]["right"] or not sprites["walking"]["right"]:
                raise ValueError("Missing required sprites")
                
        except Exception as e:
            add_debug(f"Player: Error during sprite loading: {e}")
            self.create_fallback_sprites(sprites)
        
        return sprites
    
    def create_fallback_sprites(self, sprites):
        """Create simple rectangle sprites as fallbacks"""
        add_debug("Player: Creating fallback sprite rectangles")
        
        # For each animation state and direction, create simple rectangular sprites
        for state in ["idle", "walking"]:
            for direction in ["right", "left"]:
                # Clear any partially loaded sprites
                sprites[state][direction] = []
                
                # Create 4 frames for each state
                for i in range(4):
                    # Create base sprite
                    sprite = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
                    sprite.fill(GREEN)
                    
                    # Add a detail line that moves to show animation
                    line_y = 10 + (i * 10) if state == "walking" else PLAYER_HEIGHT // 2
                    line_color = (255, 255, 255)  # White line
                    
                    # For left-facing, draw line on left side
                    if direction == "left":
                        pygame.draw.line(sprite, line_color, 
                                        (0, line_y), (PLAYER_WIDTH // 2, line_y), 2)
                    else:
                        pygame.draw.line(sprite, line_color, 
                                        (PLAYER_WIDTH // 2, line_y), (PLAYER_WIDTH, line_y), 2)
                    
                    sprites[state][direction].append(sprite)
        
        add_debug("Player: Fallback sprites created")
    
    def move(self, platforms, camera_offset_x):
        """Update player position and handle collisions"""
        # Set default animation state
        self.animation_state = "idle"
        
        # Horizontal movement
        if self.moving_left:
            self.x -= self.speed
            self.facing_right = False  # Ensure player faces left when moving left
            self.animation_state = "walking"
        if self.moving_right:
            self.x += self.speed
            self.facing_right = True  # Ensure player faces right when moving right
            self.animation_state = "walking"
        
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
            self.y = GROUND_LEVEL - self.height  # Ensure player is exactly on ground level
            self.velocity_y = 0
            self.on_ground = True
        
        # Keep player within left boundary
        if self.x < 0:
            self.x = 0
        
        # Update animation timer
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            # Make sure we don't go out of index range
            max_frames = len(self.sprites[self.animation_state]["right"])
            self.frame_index = (self.frame_index + 1) % max_frames if max_frames > 0 else 0
        
        # Update hit effect timer
        if self.is_hit:
            self.hit_timer += 1
            if self.hit_timer >= 10:  # Flash for 10 frames
                self.is_hit = False
                self.hit_timer = 0
    
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
        
        # Update facing direction based on mouse position
        # Note: Only update direction if the player isn't moving
        if not (self.moving_left or self.moving_right):
            if dir_x > 0:
                self.facing_right = True
            else:
                self.facing_right = False
        
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
        self.is_hit = True
        self.hit_timer = 0
    
    def draw(self, screen, debug_mode=False):
        """Draw the player on the screen"""
        if self.use_sprites:
            # Get the current sprite based on animation state and direction
            direction = "right" if self.facing_right else "left"
            
            # Safeguard against potential index errors
            if (self.animation_state in self.sprites and 
                direction in self.sprites[self.animation_state] and 
                len(self.sprites[self.animation_state][direction]) > 0):
                
                # Make sure frame index is valid
                if self.frame_index >= len(self.sprites[self.animation_state][direction]):
                    self.frame_index = 0
                
                current_sprite = self.sprites[self.animation_state][direction][self.frame_index]
                sprite_width, sprite_height = current_sprite.get_size()
                
                # Calculate position to center sprite horizontally and align bottom with player's feet
                sprite_x = self.x + (self.width - sprite_width) / 2
                sprite_y = self.y + self.height - sprite_height  # Position bottom of sprite at player's feet
                
                # Apply hit effect (flash red) if player was recently hit
                if self.is_hit:
                    # Create a copy of the sprite to modify
                    hit_sprite = current_sprite.copy()
                    
                    # Create red overlay
                    red_overlay = pygame.Surface(hit_sprite.get_size(), pygame.SRCALPHA)
                    red_overlay.fill((255, 0, 0, 128))  # Red with 50% transparency
                    
                    # Apply overlay to sprite
                    hit_sprite.blit(red_overlay, (0, 0))
                    
                    # Draw the hit sprite
                    screen.blit(hit_sprite, (int(sprite_x), int(sprite_y)))
                else:
                    # Draw normal sprite
                    screen.blit(current_sprite, (int(sprite_x), int(sprite_y)))
            else:
                # Fallback if sprites aren't properly loaded
                self._draw_fallback(screen)
        else:
            # Use fallback drawing if sprites are disabled
            self._draw_fallback(screen)
        
        # Draw debug info
        if debug_mode:
            # Draw collision box
            pygame.draw.rect(screen, (255, 0, 255), 
                        (self.x, self.y, self.width, self.height), 1)
            
            # Draw reference points at the bottom center of player
            pygame.draw.circle(screen, (255, 0, 0), 
                            (int(self.x + self.width/2), int(self.y + self.height)), 3)
    
    def _draw_fallback(self, screen):
        """Draw a simple colored rectangle as fallback"""
        # Draw the player as a colored rectangle
        color = (255, 0, 0) if self.is_hit else GREEN
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Add a direction indicator
        eye_x = self.x + (3*self.width//4 if self.facing_right else self.width//4)
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x), int(self.y + self.height//4)), 5)