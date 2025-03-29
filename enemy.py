import pygame
import random
import math
import os
from settings import (
    ZOMBIE_WIDTH, ZOMBIE_HEIGHT, ZOMBIE_SPEED, ZOMBIE_MAX_HEALTH,
    ZOMBIE_DAMAGE, ZOMBIE_ATTACK_COOLDOWN, BROWN, RED, GRAVITY,
    GROUND_LEVEL, WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT
)
from debug import add_debug

class Zombie:
    """Basic zombie enemy that moves toward the player"""
    
    def __init__(self, x, y):
        # Calculate better size to match player proportions
        # Make zombies slightly smaller than player but not too small
        self.width = int(PLAYER_WIDTH * 0.9)  # 90% of player width
        self.height = int(PLAYER_HEIGHT * 0.9)  # 90% of player height
        
        self.x = x  # World x position
        self.y = y
        self.speed = ZOMBIE_SPEED
        self.health = ZOMBIE_MAX_HEALTH
        self.max_health = ZOMBIE_MAX_HEALTH
        self.damage = ZOMBIE_DAMAGE
        self.attack_cooldown = 0
        self.attack_cooldown_max = ZOMBIE_ATTACK_COOLDOWN
        self.color = BROWN  # Fallback color
        self.velocity_y = 0
        self.on_ground = False
        
        # Animation properties
        self.facing_right = True
        self.animation_state = "run"  # run, idle, attack
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_delay = 10  # Frames between sprite changes
        
        # Attack state
        self.is_attacking = False
        self.attack_frame = 0
        self.attack_duration = 40  # Frames for attack animation
        
        # Damage flash effect
        self.is_hit = False
        self.hit_timer = 0
        
        # Load sprites
        self.use_sprites = True
        self.sprites = self.load_sprites()
        
        # Frame counts
        self.frame_counts = {
            "run": 4,   # 4 frames in run animation
            "idle": 2,  # 2 frames in idle animation
            "attack": 4 # 4 frames in attack animation
        }
    
    def load_sprites(self):
        """Load all zombie sprite images"""
        add_debug("Zombie: Loading sprites...")
        
        sprites = {
            "run": {
                "right": [],
                "left": []
            },
            "idle": {
                "right": [],
                "left": []
            },
            "attack": {
                "right": [],
                "left": []
            }
        }
        
        # Check if we have the sprites directory
        enemy_sprite_dir = "assets/enemy"
        if not os.path.exists(enemy_sprite_dir):
            add_debug("Zombie: 'assets/enemy' directory not found!")
            self.use_sprites = False
            return sprites
        
        try:
            # Load animations with the correct frame counts
            animation_frames = {
                "run": 4,
                "idle": 2,
                "attack": 4
            }
            
            # Load all animation types and directions
            for anim, frame_count in animation_frames.items():
                for direction in ["right", "left"]:
                    # Load all frames for this animation/direction
                    for i in range(frame_count):
                        sprite_path = f"{enemy_sprite_dir}/zombie_{anim}_{direction}_{i}.png"
                        if os.path.exists(sprite_path):
                            original_sprite = pygame.image.load(sprite_path).convert_alpha()
                            
                            # Scale sprite to match the proportions we want
                            scaled_sprite = pygame.transform.scale(original_sprite, (self.width, self.height))
                            sprites[anim][direction].append(scaled_sprite)
                            add_debug(f"Zombie: Loaded {sprite_path}")
                        else:
                            add_debug(f"Zombie: Missing sprite {sprite_path}")
            
            # Verify we have at least run animation
            if not sprites["run"]["right"] or not sprites["run"]["left"]:
                add_debug("Zombie: Missing required run animation sprites")
                self.use_sprites = False
            
            return sprites
            
        except Exception as e:
            add_debug(f"Zombie: Error loading sprites: {e}")
            self.use_sprites = False
            return sprites
    
    def update(self, player_world_x, platforms):
        """Update zombie position and state"""
        # Only move if not attacking
        if not self.is_attacking:
            # Determine facing direction based on player position
            if self.x < player_world_x:
                self.x += self.speed
                self.facing_right = True
                self.animation_state = "run"
            else:
                self.x -= self.speed
                self.facing_right = False
                self.animation_state = "run"
                
            # If close to player, start attack
            if abs(self.x - player_world_x) < 50:
                self.start_attack()
        else:
            # Handle attack state
            self.animation_state = "attack"
            self.attack_frame += 1
            if self.attack_frame >= self.attack_duration:
                self.is_attacking = False
                self.attack_frame = 0
                self.animation_state = "run"
        
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
            
        # Update animation timer
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            
            # Calculate next frame index based on animation state
            if self.animation_state in self.sprites and self.use_sprites:
                direction = "right" if self.facing_right else "left"
                if direction in self.sprites[self.animation_state]:
                    # Get correct frame count for this animation
                    max_frames = len(self.sprites[self.animation_state][direction])
                    if max_frames > 0:
                        self.frame_index = (self.frame_index + 1) % max_frames
                    
        # Update hit effect timer
        if self.is_hit:
            self.hit_timer += 1
            if self.hit_timer >= 5:  # Flash for 5 frames
                self.is_hit = False
                self.hit_timer = 0
    
    def start_attack(self):
        """Start the attack animation"""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_frame = 0
            self.frame_index = 0  # Reset frame index for attack animation
    
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
            # Start attack animation
            self.start_attack()
            
            # Deal damage
            player.take_damage(self.damage)
            self.attack_cooldown = self.attack_cooldown_max
            add_debug(f"Player hit! Health: {player.health}")
            return True
        return False
    
    def take_damage(self, amount):
        """Reduce zombie health by the given amount"""
        self.health -= amount
        self.is_hit = True
        self.hit_timer = 0
        
        # If health is low, switch to idle animation briefly
        if self.health < self.max_health / 2 and not self.is_attacking:
            self.animation_state = "idle"
    
    def draw(self, screen, camera_offset_x, debug_mode=False):
        """Draw the zombie on the screen"""
        # Calculate screen position
        screen_x = self.x - camera_offset_x
        
        # Only draw if on screen (with a margin)
        if -self.width < screen_x < WIDTH + self.width:
            if self.use_sprites:
                # Determine which direction sprites to use
                direction = "right" if self.facing_right else "left"
                
                # Make sure we have sprites for this animation state and direction
                if (self.animation_state in self.sprites and 
                    direction in self.sprites[self.animation_state] and 
                    self.sprites[self.animation_state][direction]):
                    
                    # Make sure frame index is valid
                    if self.frame_index >= len(self.sprites[self.animation_state][direction]):
                        self.frame_index = 0
                    
                    # Get current sprite
                    current_sprite = self.sprites[self.animation_state][direction][self.frame_index]
                    
                    # Apply hit effect if needed
                    if self.is_hit:
                        # Draw sprite with red tint for hit effect
                        hit_color = (255, 0, 0)
                        screen.blit(current_sprite, (int(screen_x), int(self.y)))
                        # Draw a semi-transparent red rect over it for the hit effect
                        hit_surface = pygame.Surface((self.width, self.height))
                        hit_surface.fill(hit_color)
                        hit_surface.set_alpha(128)  # 50% transparency
                        screen.blit(hit_surface, (int(screen_x), int(self.y)))
                    else:
                        # Draw normal sprite
                        screen.blit(current_sprite, (int(screen_x), int(self.y)))
                else:
                    # Fallback to rectangle if no sprites for this animation/direction
                    self._draw_fallback(screen, screen_x)
            else:
                # Use fallback drawing
                self._draw_fallback(screen, screen_x)
            
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
            
            # Debug: Draw collision box and state
            if debug_mode:
                pygame.draw.rect(screen, (255, 0, 255), 
                                (screen_x, self.y, self.width, self.height), 1)  # Draw outline
                
                # Draw state text
                debug_font = pygame.font.Font(None, 20)
                state_text = f"{self.animation_state}"
                text_surf = debug_font.render(state_text, True, (255, 255, 255))
                screen.blit(text_surf, (screen_x, self.y - 25))
    
    def _draw_fallback(self, screen, screen_x):
        """Draw fallback rectangle if sprites aren't available"""
        color = RED if self.is_hit else BROWN
        pygame.draw.rect(screen, color, (screen_x, self.y, self.width, self.height))
        
        # Add simple direction indicator
        if self.facing_right:
            # Right-facing indicator
            pygame.draw.circle(screen, (255, 255, 255), 
                              (int(screen_x + 3*self.width//4), int(self.y + self.height//4)), 3)
        else:
            # Left-facing indicator
            pygame.draw.circle(screen, (255, 255, 255), 
                              (int(screen_x + self.width//4), int(self.y + self.height//4)), 3)

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