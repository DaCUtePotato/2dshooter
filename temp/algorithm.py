import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Original tile dimensions
ORIGINAL_TILE_SIZE = 476

# Load tile image
tile_image = pygame.image.load('tile.png')

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

def get_scaled_tile(zoom):
    """ Return the tile image scaled according to the zoom level. """
    scaled_size = int(ORIGINAL_TILE_SIZE * zoom)
    return pygame.transform.scale(tile_image, (scaled_size, scaled_size)), scaled_size

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

    # Get the scaled tile image and size
    scaled_tile_image, TILE_SIZE = get_scaled_tile(zoom)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the tiles
    start_x = -(camera_x % TILE_SIZE)
    start_y = -(camera_y % TILE_SIZE)

    for y in range(start_y, SCREEN_HEIGHT, TILE_SIZE):
        for x in range(start_x, SCREEN_WIDTH, TILE_SIZE):
            screen.blit(scaled_tile_image, (x, y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to the monitor's refresh rate (vSync)
    clock.tick(60)  # Assuming a 60 Hz monitor

# Quit Pygame
pygame.quit()
sys.exit()
