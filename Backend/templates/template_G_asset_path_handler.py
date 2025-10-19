import os
import sys
import pygame

# --- Constants & Initialization (Assumed from A) ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Template G: Asset Path Handler")
clock = pygame.time.Clock()
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 36)

# --- Asset Path Handler Function ---
def resource_path(relative_path):
    """
    Get the absolute path to resource, works for dev and for PyInstaller.
    
    During development, it returns the path relative to the script.
    When compiled by PyInstaller, it returns the path inside the bundled MEIPASS folder.
    """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Not running as a compiled executable, use the current script directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- Placeholder Asset Usage ---
# NOTE: This example requires you to create a dummy 'assets' folder with a 'test.txt' 
# and a 'player.png' file in the same directory as this script for the paths to work in dev mode.

# Example 1: Load a text file (using the handler)
asset_status_text = "Asset Path Status: Loading..."
try:
    # Assume we are trying to load an asset located at 'assets/test.txt'
    text_file_path = resource_path(os.path.join('assets', 'test.txt'))
    
    # Check if the path points to an existing file (optional, but good for debugging)
    if os.path.exists(text_file_path):
        with open(text_file_path, 'r') as f:
            content = f.read().strip()
            asset_status_text = f"Text Asset Loaded: '{content}'"
    else:
        # If running in dev mode, this path won't exist until you create the 'assets' folder/file
        asset_status_text = "Asset Path Handler OK. Placeholder file not found."

except Exception as e:
    asset_status_text = f"Error loading asset: {e}"


# Example 2: Load an image (using the handler)
image_path = resource_path(os.path.join('assets', 'player.png'))
# Creating a dummy image surface since we can't guarantee 'player.png' exists
try:
    if os.path.exists(image_path):
        player_img = pygame.image.load(image_path).convert_alpha()
    else:
        # Fallback to a solid color square if image not found
        player_img = pygame.Surface((50, 50))
        player_img.fill(RED)
except Exception:
    player_img = pygame.Surface((50, 50))
    player_img.fill(RED)
    
player_rect = player_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. Update
    
    # 2. Drawing
    screen.fill(WHITE)
    
    # Draw the player image/placeholder
    screen.blit(player_img, player_rect)
    
    # Display the status of the asset path handler
    status_surface = FONT.render(asset_status_text, True, (0, 0, 0))
    path_info = FONT.render(f"Path Check: {'_MEIPASS' in sys.modules and sys.frozen}", True, (0, 0, 0))
    
    screen.blit(status_surface, (50, 50))
    screen.blit(path_info, (50, 100))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
