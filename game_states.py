"""
Game state management system
"""
import pygame
import sys
from settings import (
    MENU, GAMEPLAY, PAUSE, GAMEOVER, CONTROLS, LEVELSELECT, VICTORY,
    MENU_OPTIONS, LEVEL_OPTIONS, PAUSE_OPTIONS, GAMEOVER_OPTIONS, VICTORY_OPTIONS,
    WIDTH, HEIGHT, GROUND_LEVEL, MAX_WAVES
)
from player import Player
from enemy import Zombie, spawn_wave
from ui import (
    draw_menu, draw_level_select, draw_controls, 
    draw_gameplay, draw_pause, draw_gameover, draw_victory
)
from debug import add_debug, clear_debug

# Initialize level graphics only when needed, not at module import
# This prevents loading images before pygame.display is initialized

class GameState:
    """Base class for all game states"""
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
    
    def handle_events(self, event):
        """Handle input events"""
        pass
    
    def update(self):
        """Update game state logic"""
        pass
    
    def draw(self, screen):
        """Draw the state to the screen"""
        pass

class GameStateManager:
    """Manages game states and transitions between them"""
    
    def __init__(self):
        # Initialize level graphics now that display is set up
        from level import initialize_level_graphics
        initialize_level_graphics()
        
        self.states = {
            MENU: MenuState(self),
            LEVELSELECT: LevelSelectState(self),
            CONTROLS: ControlsState(self),
            GAMEPLAY: None,  # Will be initialized when needed
            PAUSE: None,     # Will be initialized when needed
            GAMEOVER: None,  # Will be initialized when needed
            VICTORY: None    # Will be initialized when needed
        }
        self.current_state = MENU
        self.debug_mode = False
        
        # Load background image
        try:
            self.background = pygame.image.load("WCP_Example.png").convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except:
            # Create a default background if image isn't found
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((0, 0, 0))
            print("Background image not found. Using default black background.")
    
    def set_state(self, state_id, **kwargs):
        """Change to a different state"""
        if state_id == GAMEPLAY:
            if not self.states[GAMEPLAY] or kwargs.get('restart', False):
                # Initialize new gameplay state
                level = kwargs.get('level', 1)
                self.states[GAMEPLAY] = GameplayState(self, level)
        
        elif state_id == PAUSE and self.states[GAMEPLAY]:
            # Create pause state with current gameplay state
            self.states[PAUSE] = PauseState(self, self.states[GAMEPLAY])
        
        elif state_id == GAMEOVER:
            # Create game over state with final score
            score = kwargs.get('score', 0)
            self.states[GAMEOVER] = GameOverState(self, score)
            
        elif state_id == VICTORY:
            # Create victory state with score and wave count
            score = kwargs.get('score', 0)
            wave = kwargs.get('wave', MAX_WAVES)
            level = kwargs.get('level', 1)
            self.states[VICTORY] = VictoryState(self, score, wave, level)
        
        self.current_state = state_id
    
    def toggle_debug_mode(self):
        """Toggle debug mode on/off"""
        self.debug_mode = not self.debug_mode
        add_debug(f"Debug mode {'enabled' if self.debug_mode else 'disabled'}")
    
    def handle_events(self, event):
        """Pass events to current state"""
        # Global event handling for all states
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
            self.toggle_debug_mode()
        
        # Let current state handle the event
        if self.current_state in self.states and self.states[self.current_state]:
            self.states[self.current_state].handle_events(event)
    
    def update(self):
        """Update current state"""
        if self.current_state in self.states and self.states[self.current_state]:
            self.states[self.current_state].update()
    
    def draw(self, screen):
        """Draw current state"""
        if self.current_state in self.states and self.states[self.current_state]:
            self.states[self.current_state].draw(screen)

class MenuState(GameState):
    """Main menu state"""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.selected_option = 0
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(MENU_OPTIONS)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(MENU_OPTIONS)
            elif event.key == pygame.K_RETURN:
                if MENU_OPTIONS[self.selected_option] == "Play":
                    self.game_manager.set_state(GAMEPLAY, level=1, restart=True)
                elif MENU_OPTIONS[self.selected_option] == "Level Select":
                    self.game_manager.set_state(LEVELSELECT)
                elif MENU_OPTIONS[self.selected_option] == "Controls":
                    self.game_manager.set_state(CONTROLS)
                elif MENU_OPTIONS[self.selected_option] == "Exit":
                    pygame.quit()
                    sys.exit()
    
    def update(self):
        pass
    
    def draw(self, screen):
        # For menu, we'll still use the provided background
        draw_menu(screen, self.game_manager.background, self.selected_option)

class LevelSelectState(GameState):
    """Level selection state"""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.selected_option = 0
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(LEVEL_OPTIONS)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(LEVEL_OPTIONS)
            elif event.key == pygame.K_RETURN:
                if LEVEL_OPTIONS[self.selected_option] == "Level 1":
                    self.game_manager.set_state(GAMEPLAY, level=1, restart=True)
                elif LEVEL_OPTIONS[self.selected_option] == "Back":
                    self.game_manager.set_state(MENU)
                # Level 2 is locked - do nothing
            elif event.key == pygame.K_ESCAPE:
                self.game_manager.set_state(MENU)
    
    def update(self):
        pass
    
    def draw(self, screen):
        draw_level_select(screen, self.game_manager.background, self.selected_option)

class ControlsState(GameState):
    """Controls display state"""
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_manager.set_state(MENU)
    
    def update(self):
        pass
    
    def draw(self, screen):
        draw_controls(screen)

class GameplayState(GameState):
    """Main gameplay state"""
    
    def __init__(self, game_manager, level=1):
        super().__init__(game_manager)
        self.level = level
        
        # Player setup
        self.player = Player(100, GROUND_LEVEL - 60)
        
        # Level setup
        from level import create_level
        self.platforms, self.obstacles = create_level(level)
        
        # Game elements
        self.enemies = []
        self.projectiles = []
        
        # Game state
        self.score = 0
        self.wave = 1
        self.wave_enemies_remaining = 5 + self.wave
        self.camera_offset_x = 0
        
        # Spawn initial wave
        self.enemies = spawn_wave(
            self.player.x, 
            self.camera_offset_x, 
            self.wave_enemies_remaining
        )
        
        # Clear any old debug messages
        clear_debug()
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player.moving_left = True
            elif event.key == pygame.K_d:
                self.player.moving_right = True
            elif event.key == pygame.K_SPACE and self.player.on_ground:
                self.player.jump()
            elif event.key == pygame.K_ESCAPE:
                self.game_manager.set_state(PAUSE)
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.player.moving_left = False
            elif event.key == pygame.K_d:
                self.player.moving_right = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.player.shoot(pygame.mouse.get_pos(), self.camera_offset_x, self.projectiles)
    
    def update(self):
        # Update player
        self.player.move(self.platforms, self.camera_offset_x)
        
        # Camera follows player - side-scrolling effect
        # Camera only moves right when player is past 1/3 of screen
        if self.player.x > WIDTH / 3:
            self.camera_offset_x += self.player.x - WIDTH / 3
            self.player.x = WIDTH / 3  # Keep player position fixed on screen
        
        # Check obstacles for player collision
        player_world_x = self.player.x + self.camera_offset_x
        for obstacle in self.obstacles:
            if obstacle.check_collision(player_world_x, self.player.y, self.player.width, self.player.height):
                # If obstacle blocks player, push them back
                if obstacle.blocks_player:
                    # Push left or right depending on approach direction
                    if player_world_x < obstacle.x + obstacle.width / 2:
                        # Push player left
                        correction = obstacle.x - (player_world_x + self.player.width)
                        self.player.x += correction
                    else:
                        # Push player right
                        correction = (obstacle.x + obstacle.width) - player_world_x
                        self.player.x += correction
                
                # If obstacle damages player
                if obstacle.damage > 0:
                    self.player.take_damage(obstacle.damage)
                    add_debug(f"Player hit obstacle! Damage: {obstacle.damage}")
                    
                    # Check if player is dead
                    if self.player.health <= 0:
                        self.game_manager.set_state(GAMEOVER, score=self.score)
        
        # Update enemies
        for enemy in self.enemies[:]:
            # Calculate player's world position
            player_world_x = self.player.x + self.camera_offset_x
            
            # Update enemy
            enemy.update(player_world_x, self.platforms)
            
            # Check for enemy collision with obstacles
            for obstacle in self.obstacles:
                if obstacle.blocks_enemies and obstacle.check_collision(
                    enemy.x, enemy.y, enemy.width, enemy.height
                ):
                    # Simple bounce logic - reverse direction
                    if enemy.x < obstacle.x:
                        enemy.x -= enemy.speed * 2
                    else:
                        enemy.x += enemy.speed * 2
            
            # Check for collision with player
            if enemy.check_collision_with_player(
                self.player.x, self.player.y, 
                self.player.width, self.player.height, 
                self.camera_offset_x
            ):
                # Attack player
                if enemy.attack_player(self.player):
                    # Check if player is dead
                    if self.player.health <= 0:
                        self.game_manager.set_state(GAMEOVER, score=self.score)
        
        # Update projectiles and check for offscreen/age
        for projectile in self.projectiles[:]:
            projectile.update()
            
            # Check for collision with obstacles
            for obstacle in self.obstacles:
                if obstacle.blocks_projectiles and obstacle.check_collision(
                    projectile.x, projectile.y, projectile.radius*2, projectile.radius*2
                ):
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break
            
            # Skip if projectile was removed by obstacle
            if projectile not in self.projectiles:
                continue
            
            # Remove projectiles that are too old or off-screen
            if projectile.is_offscreen(self.camera_offset_x, WIDTH, HEIGHT):
                self.projectiles.remove(projectile)
                continue
            
            # Check for collisions with enemies
            for enemy in self.enemies[:]:
                if projectile.check_collision(enemy):
                    enemy.take_damage(projectile.damage)
                    
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.score += 100
                        add_debug(f"Enemy killed! Score: {self.score}")
                    
                    break
        
        # Check if wave is completed
        if not self.enemies:
            self.wave += 1
            
            # Check for victory condition
            if self.wave > MAX_WAVES:
                add_debug("Victory! All waves completed!")
                self.game_manager.set_state(VICTORY, score=self.score, wave=self.wave-1, level=self.level)
            else:
                self.wave_enemies_remaining = 5 + self.wave
                self.enemies = spawn_wave(
                    self.player.x, 
                    self.camera_offset_x, 
                    self.wave_enemies_remaining
                )
                add_debug(f"Wave {self.wave}/{MAX_WAVES} started! Enemies: {self.wave_enemies_remaining}")
    
    def draw(self, screen):
        """Draw the gameplay state"""
        from level import draw_level_background
        
        # Draw level background with parallax effect
        draw_level_background(screen, self.camera_offset_x, self.game_manager.debug_mode)

        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(screen, self.camera_offset_x)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(screen, self.camera_offset_x)
        
        # Draw player
        self.player.draw(screen, self.game_manager.debug_mode)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen, self.camera_offset_x, self.game_manager.debug_mode)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen, self.camera_offset_x, self.game_manager.debug_mode)
        
        # Draw UI elements - use the function name that's actually defined in ui.py
        from ui import draw_gameplay
        draw_gameplay(screen, self.player, self.platforms, self.obstacles, self.enemies, 
                    self.projectiles, self.score, self.wave, self.camera_offset_x,
                    self.game_manager.debug_mode)

class GameOverState(GameState):
    """Game over state showing score and restart options"""
    
    def __init__(self, game_manager, score):
        super().__init__(game_manager)
        self.score = score
        self.selected_option = 0
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(GAMEOVER_OPTIONS)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(GAMEOVER_OPTIONS)
            elif event.key == pygame.K_RETURN:
                if GAMEOVER_OPTIONS[self.selected_option] == "Try Again":
                    self.game_manager.set_state(GAMEPLAY, restart=True)
                elif GAMEOVER_OPTIONS[self.selected_option] == "Main Menu":
                    self.game_manager.set_state(MENU)
    
    def update(self):
        pass
    
    def draw(self, screen):
        draw_gameover(screen, self.score, self.selected_option)

class PauseState(GameState):
    """Pause menu state"""
    
    def __init__(self, game_manager, gameplay_state):
        super().__init__(game_manager)
        self.gameplay_state = gameplay_state
        self.selected_option = 0
        
        # Create a screenshot of the current gameplay
        self.gameplay_screen = pygame.Surface((WIDTH, HEIGHT))
        self.gameplay_screen.blit(pygame.display.get_surface(), (0, 0))
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Resume game when ESC is pressed again
                self.game_manager.current_state = GAMEPLAY
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(PAUSE_OPTIONS)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(PAUSE_OPTIONS)
            elif event.key == pygame.K_RETURN:
                if PAUSE_OPTIONS[self.selected_option] == "Resume":
                    self.game_manager.current_state = GAMEPLAY
                elif PAUSE_OPTIONS[self.selected_option] == "Controls":
                    self.game_manager.set_state(CONTROLS)
                elif PAUSE_OPTIONS[self.selected_option] == "Quit to Menu":
                    self.game_manager.set_state(MENU)
    
    def update(self):
        pass
    
    def draw(self, screen):
        draw_pause(screen, self.gameplay_screen, self.selected_option)

class VictoryState(GameState):
    """Victory state showing score and completion info"""
    
    def __init__(self, game_manager, score, wave, level):
        super().__init__(game_manager)
        self.score = score
        self.wave = wave
        self.level = level
        self.selected_option = 0
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(VICTORY_OPTIONS)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(VICTORY_OPTIONS)
            elif event.key == pygame.K_RETURN:
                if VICTORY_OPTIONS[self.selected_option] == "Next Level":
                    # Try to load next level or go to menu if there is no next level
                    next_level = self.level + 1
                    if next_level <= 2:  # Assuming we have 2 levels
                        self.game_manager.set_state(GAMEPLAY, level=next_level, restart=True)
                    else:
                        # No more levels, go back to menu
                        self.game_manager.set_state(MENU)
                elif VICTORY_OPTIONS[self.selected_option] == "Main Menu":
                    self.game_manager.set_state(MENU)
    
    def update(self):
        pass
    
    def draw(self, screen):
        draw_victory(screen, self.score, self.wave, self.selected_option)