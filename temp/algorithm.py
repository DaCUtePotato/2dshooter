import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Original tile dimensions
ORIGINAL_TILE_SIZE = 476

# Load tile images for different types
tile_images = {
    "up-left": pygame.image.load('dirt/Dirt12.png'),
    "up": pygame.image.load('dirt/Dirt4.png'),
    "up-right": pygame.image.load('dirt/Dirt10.png'),
    "left": pygame.image.load('dirt/Dirt2.png'),
    "center": pygame.image.load('dirt/Dirt0.png'),
    "right": pygame.image.load('dirt/Dirt7.png'),
    "down-left": pygame.image.load('dirt/Dirt11.png'),
    "down": pygame.image.load('dirt/Dirt5.png'),
    "down-right": pygame.image.load('dirt/Dirt9.png')
}

# Create the screen with vSync enabled
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption('Scrolling Background with vSync')

# Camera position
camera_x, camera_y = 0, 0

# Movement speed
speed = 20

# Zoom level (1.0 means 100%)
zoom = 1.0

# Set up the clock for vSync
clock = pygame.time.Clock()

def get_scaled_tile(tile_type, zoom):
    """ Return the tile image scaled according to the zoom level. """
    scaled_size = int(ORIGINAL_TILE_SIZE * zoom)
    return pygame.transform.scale(tile_images[tile_type], (scaled_size, scaled_size)), scaled_size

def get_random_tile_type():
    """ Return a random tile type. """
    return random.choice(list(tile_images.keys()))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                zoom *= 1.1  # Zoom in
            elif event.key == pygame.K_MINUS:
                zoom /= 1.1  # Zoom out

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_y -= speed
    if keys[pygame.K_s]:
        camera_y += speed
    if keys[pygame.K_a]:
        camera_x -= speed
    if keys[pygame.K_d]:
        camera_x += speed

    # Get the scaled tile size
    _, TILE_SIZE = get_scaled_tile("center", zoom)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Calculate the start position to draw tiles, ensuring they cover the entire screen
    start_x = -(camera_x % TILE_SIZE)
    start_y = -(camera_y % TILE_SIZE)

    # Calculate the offset for the top-left corner of the visible area
    offset_x = camera_x // TILE_SIZE
    offset_y = camera_y // TILE_SIZE

    # Draw the tiles
    for y in range(-1, SCREEN_HEIGHT // TILE_SIZE + 2):
        for x in range(-1, SCREEN_WIDTH // TILE_SIZE + 2):
            tile_type = get_random_tile_type()
            scaled_tile_image, _ = get_scaled_tile(tile_type, zoom)
            screen_x = start_x + x * TILE_SIZE
            screen_y = start_y + y * TILE_SIZE
            screen.blit(scaled_tile_image, (screen_x, screen_y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to the monitor's refresh rate (vSync)
    clock.tick(60)  # Assuming a 60 Hz monitor

# Quit Pygame
pygame.quit()
sys.exit()
