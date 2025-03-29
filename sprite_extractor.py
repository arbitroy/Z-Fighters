import os
import pygame

# Initialize pygame so we can use its image functions
pygame.init()

# Create directory for enemy sprites
if not os.path.exists("assets/enemy"):
    os.makedirs("assets/enemy")
    print("Created assets/enemy directory")

def extract_sprites(spritesheet_path, animation_type, frame_width=32):
    """
    Extract individual frames from a spritesheet
    
    Args:
        spritesheet_path: Path to the spritesheet image
        animation_type: Animation type (run, idle, attack)
        frame_width: Width of each frame in pixels (default: 32)
    """
    # Load the spritesheet
    try:
        spritesheet = pygame.image.load(spritesheet_path)
        sheet_width, sheet_height = spritesheet.get_size()
        
        print(f"Processing {spritesheet_path}: {sheet_width}x{sheet_height}")
        
        # Calculate number of frames based on sheet width and frame width
        num_frames = sheet_width // frame_width
        print(f"Detected {num_frames} frames")
        
        # For each frame in the spritesheet
        for i in range(num_frames):
            # Extract the frame
            frame_x = i * frame_width
            frame_rect = pygame.Rect(frame_x, 0, frame_width, sheet_height)
            frame = spritesheet.subsurface(frame_rect)
            
            # Save the right-facing frame
            right_filename = f"assets/enemy/zombie_{animation_type}_right_{i}.png"
            pygame.image.save(frame, right_filename)
            print(f"Saved {right_filename}")
            
            # Create and save left-facing frame (flipped horizontally)
            left_frame = pygame.transform.flip(frame, True, False)
            left_filename = f"assets/enemy/zombie_{animation_type}_left_{i}.png"
            pygame.image.save(left_frame, left_filename)
            print(f"Saved {left_filename}")
            
    except Exception as e:
        print(f"Error processing {spritesheet_path}: {e}")

# Base path to the zombie sprite sheets
base_path = "C:/Users/eProd/Git/Z-Fighters/Zombie Asset Pack/enemies/zombie"

# Define the sprite sheets to process with appropriate frame info
sprite_data = [
    {
        "path": os.path.join(base_path, "zombie_run.png"),
        "animation": "run",
        "frame_width": 32  # 128 pixels wide, 4 frames = 32px per frame
    },
    {
        "path": os.path.join(base_path, "zombie_idle.png"),
        "animation": "idle",
        "frame_width": 32  # 64 pixels wide, 2 frames = 32px per frame
    },
    {
        "path": os.path.join(base_path, "zombie_attack.png"),
        "animation": "attack",
        "frame_width": 32  # 128 pixels wide, 4 frames = 32px per frame
    }
]

# Process all spritesheets
for data in sprite_data:
    if os.path.exists(data["path"]):
        extract_sprites(
            data["path"],
            data["animation"],
            data["frame_width"]
        )
    else:
        print(f"Warning: Spritesheet {data['path']} not found")

print("Sprite extraction complete!")