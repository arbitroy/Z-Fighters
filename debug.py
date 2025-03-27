"""
Debug utilities for displaying debug information and logging to file
"""
import pygame
import os
import time
from settings import DEBUG_FONT, WHITE, BLACK, WIDTH, HEIGHT

# Global debug messages list
debug_messages = []

# Set up file logging
log_file = "debug_log.txt"

# Clear the log file when the game starts
try:
    with open(log_file, 'w') as f:
        f.write(f"=== Debug Log Started at {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
except Exception as e:
    print(f"Error initializing log file: {e}")

def log_to_file(message):
    """Write a message to the log file"""
    try:
        with open(log_file, 'a') as f:
            f.write(f"{message}\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def add_debug(message):
    """Add a debug message to the list and log to file"""
    global debug_messages
    # Add timestamp to the message
    timestamp = time.strftime("%H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    
    # Log to file
    log_to_file(formatted_message)
    
    # Add to on-screen messages
    debug_messages.append(message)  # Don't show timestamp on screen to save space
    if len(debug_messages) > 10:  # Keep only the last 10 messages
        debug_messages.pop(0)

def clear_debug():
    """Clear all debug messages"""
    global debug_messages
    debug_messages.clear()
    log_to_file("--- Debug messages cleared ---")

def draw_debug_info(screen, player, camera_offset_x, enemies, projectiles):
    """Draw debug information on the screen"""
    # Draw debug panel background
    pygame.draw.rect(screen, (0, 0, 0, 128), (WIDTH - 300, 10, 290, 200))
    
    # Draw game state info
    debug_info = [
        f"Player Pos: ({player.x:.1f}, {player.y:.1f})",
        f"World Pos: ({(player.x + camera_offset_x):.1f}, {player.y:.1f})",
        f"Camera Offset: {camera_offset_x:.1f}",
        f"Enemies: {len(enemies)}",
        f"Projectiles: {len(projectiles)}",
        f"On Ground: {player.on_ground}",
        f"Health: {player.health}"
    ]
    
    y_pos = 15
    for info in debug_info:
        text = DEBUG_FONT.render(info, True, WHITE)
        screen.blit(text, (WIDTH - 290, y_pos))
        y_pos += 20
    
    # Draw recent debug messages
    y_pos = HEIGHT - 30 * len(debug_messages) - 10
    for msg in debug_messages:
        text = DEBUG_FONT.render(msg, True, WHITE)
        screen.blit(text, (10, y_pos))
        y_pos += 20