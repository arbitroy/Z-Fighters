"""
UI rendering functions for different game states
"""
import pygame
from settings import (
    TITLE_FONT, MENU_FONT, UI_FONT, WIDTH, HEIGHT, 
    RED, WHITE, YELLOW, BLACK, MENU_OPTIONS, LEVEL_OPTIONS,
    PAUSE_OPTIONS, GAMEOVER_OPTIONS, VICTORY_OPTIONS, MAX_WAVES
)
from debug import draw_debug_info

def draw_menu(screen, background, selected_option):
    """Draw the main menu screen"""
    screen.blit(background, (0, 0))
    
    # Title
    title_text = TITLE_FONT.render("Zombie Fighters", True, YELLOW)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    
    # Menu options
    for i, option in enumerate(MENU_OPTIONS):
        color = RED if i == selected_option else WHITE
        text = MENU_FONT.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 60))

def draw_level_select(screen, background, selected_option):
    """Draw the level selection screen"""
    screen.blit(background, (0, 0))
    
    # Title
    title_text = TITLE_FONT.render("Select Level", True, YELLOW)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    
    # Level options
    for i, option in enumerate(LEVEL_OPTIONS):
        # Use gray for locked level
        if option == "Level 2 (Locked)":
            color = (128, 128, 128)  # Gray
        else:
            color = RED if i == selected_option else WHITE
        
        text = MENU_FONT.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 60))

def draw_controls(screen):
    """Draw the controls screen"""
    screen.fill(BLACK)
    
    # Title
    title_text = TITLE_FONT.render("Controls", True, YELLOW)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    
    # Controls information
    controls = [
        "A - Move Left",
        "D - Move Right",
        "SPACE - Jump",
        "Left Click - Shoot",
        "ESC - Pause Game",
        "F3 - Toggle Debug Mode"
    ]
    
    for i, control in enumerate(controls):
        text = MENU_FONT.render(control, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + i * 50))
    
    # Back instructions
    back_text = MENU_FONT.render("Press ESC to return", True, RED)
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, 500))

def draw_health_bar(screen, player):
    """Draw the player's health bar"""
    health_bar_width = 200
    health_percentage = max(0, player.health / player.max_health)
    health_width = int(health_bar_width * health_percentage)
    
    # Health bar background
    pygame.draw.rect(screen, (100, 100, 100), (10, 10, health_bar_width, 20))
    # Health bar
    pygame.draw.rect(screen, RED, (10, 10, health_width, 20))
    
    # Health text
    health_text = UI_FONT.render(f"Health: {player.health}/{player.max_health}", True, WHITE)
    screen.blit(health_text, (10, 40))

def draw_gameplay_ui(screen, player, score, wave):
    """Draw the in-game UI elements"""
    # Draw health bar
    draw_health_bar(screen, player)
    
    # Draw score
    score_text = UI_FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 70))
    
    # Draw wave counter
    wave_text = UI_FONT.render(f"Wave: {wave}/{MAX_WAVES}", True, WHITE)
    screen.blit(wave_text, (10, 100))
    
    # Draw progress bar for waves
    progress_width = 200
    progress_height = 10
    progress_x = 10
    progress_y = 130
    
    # Progress background
    pygame.draw.rect(screen, (100, 100, 100), (progress_x, progress_y, progress_width, progress_height))
    
    # Progress fill
    wave_progress = min(1.0, wave / MAX_WAVES)
    pygame.draw.rect(screen, (0, 255, 0), 
                    (progress_x, progress_y, int(progress_width * wave_progress), progress_height))

def draw_gameplay(screen, player, platforms, obstacles, enemies, projectiles, score, wave, camera_offset_x, debug_mode):
    """Draw the gameplay state"""
    from level import draw_level_background
    
    # Draw level background
    draw_level_background(screen)
    
    # Draw platforms
    for platform in platforms:
        platform.draw(screen, camera_offset_x)
    
    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw(screen, camera_offset_x)
    
    # Draw player
    player.draw(screen, debug_mode)
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen, camera_offset_x, debug_mode)
    
    # Draw projectiles
    for projectile in projectiles:
        projectile.draw(screen, camera_offset_x, debug_mode)
    
    # Draw UI elements
    draw_gameplay_ui(screen, player, score, wave)
    
    # Draw debug info if enabled
    if debug_mode:
        draw_debug_info(screen, player, camera_offset_x, enemies, projectiles)

def draw_pause(screen, gameplay_screen, selected_option):
    """Draw the pause menu over the gameplay screen"""
    # First draw the gameplay (passed as a surface)
    screen.blit(gameplay_screen, (0, 0))
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
    screen.blit(overlay, (0, 0))
    
    # Draw pause menu
    title_text = TITLE_FONT.render("Game Paused", True, YELLOW)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    
    for i, option in enumerate(PAUSE_OPTIONS):
        color = RED if i == selected_option else WHITE
        text = MENU_FONT.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 60))

def draw_gameover(screen, score, selected_option):
    """Draw the game over screen"""
    # Black background
    screen.fill(BLACK)
    
    # Game over text
    title_text = TITLE_FONT.render("Game Over", True, RED)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    
    # Score text
    score_text = MENU_FONT.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 180))
    
    # Menu options
    for i, option in enumerate(GAMEOVER_OPTIONS):
        color = RED if i == selected_option else WHITE
        text = MENU_FONT.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 300 + i * 60))

def draw_victory(screen, score, wave, selected_option):
    """Draw the victory screen"""
    # Create a gradient background (dark blue to light blue)
    for y in range(HEIGHT):
        # Calculate color based on y position
        blue_val = int(50 + (y / HEIGHT) * 150)
        pygame.draw.line(screen, (0, 0, blue_val), (0, y), (WIDTH, y))
    
    # Draw victory banner
    banner_rect = pygame.Rect(WIDTH//2 - 300, 80, 600, 100)
    pygame.draw.rect(screen, (50, 50, 100), banner_rect)
    pygame.draw.rect(screen, YELLOW, banner_rect, 3)
    
    # Victory text
    title_text = TITLE_FONT.render("VICTORY!", True, YELLOW)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    
    # Stats section
    pygame.draw.rect(screen, (0, 0, 0, 128), (WIDTH//2 - 200, 200, 400, 150))
    
    # Score and wave text
    score_text = MENU_FONT.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 220))
    
    wave_text = MENU_FONT.render(f"Waves Completed: {wave}/{MAX_WAVES}", True, WHITE)
    screen.blit(wave_text, (WIDTH // 2 - wave_text.get_width() // 2, 270))
    
    # Congratulatory message
    congrats_text = UI_FONT.render("You have defeated all the zombie waves!", True, WHITE)
    screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, 320))
    
    # Menu options
    for i, option in enumerate(VICTORY_OPTIONS):
        color = YELLOW if i == selected_option else WHITE
        text = MENU_FONT.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 400 + i * 60))