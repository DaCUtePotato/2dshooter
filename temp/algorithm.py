import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Original tile dimensions
ORIGINAL_TILE_SIZE = 16

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

# Rules for how tiles connect
tile_connections = {
    "up-left": {"bottom": ["up-left", "left", "center", "down-left"], "right": ["up-left", "up", "center", "up-right"]},
    "up": {"bottom": ["up", "center", "down"], "right": ["up", "center", "right"], "left": ["up", "center", "left"]},
    "up-right": {"bottom": ["up-right", "right", "center", "down-right"], "left": ["up-right", "up", "center", "up-left"]},
    "left": {"right": ["left", "center", "right"], "top": ["left", "down-left", "center"], "bottom": ["left", "up-left", "center"]},
    "center": {"top": ["down", "center"], "bottom": ["up", "center"], "left": ["right", "center"], "right": ["left", "center"]},
    "right": {"left": ["right", "center", "left"], "top": ["right", "down-right", "center"], "bottom": ["right", "up-right", "center"]},
    "down-left": {"top": ["down-left", "left", "center", "up-left"], "right": ["down-left", "down", "center", "down-right"]},
    "down": {"top": ["down", "center", "up"], "right": ["down", "center", "right"], "left": ["down", "center", "left"]},
    "down-right": {"top": ["down-right", "right", "center", "up-right"], "left": ["down-right", "down", "center", "down-left"]}
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

def generate_random_tile_map(width, height, seed=None):
    """ Generate a random tile map with random tile types using a seed, ensuring alignment. """
    if seed is None:
        seed = random.randint(0, 1000000)
    random.seed(seed)  # Set the seed for random number generation
    print(f"Using seed: {seed}")

    tile_types = list(tile_images.keys())
    tile_map = [[None for _ in range(width)] for _ in range(height)]

    # Fill the tile map with constraints
    for y in range(height):
        for x in range(width):
            possible_tiles = tile_types.copy()

            # Enforce bottom constraint for the tile above
            if y > 0:
                top_tile = tile_map[y - 1][x]
                possible_tiles = [tile for tile in possible_tiles if
                                  "bottom" not in tile_connections[top_tile] or tile in tile_connections[top_tile]["bottom"]]

            # Enforce right constraint for the tile to the left
            if x > 0:
                left_tile = tile_map[y][x - 1]
                possible_tiles = [tile for tile in possible_tiles if
                                  "right" not in tile_connections[left_tile] or tile in tile_connections[left_tile]["right"]]

            # Select a random tile from the possible ones
            if possible_tiles:
                selected_tile = random.choice(possible_tiles)
                tile_map[y][x] = selected_tile
            else:
                # If no tile fits the constraints, use a fallback (center tile as a default)
                tile_map[y][x] = "center"

    return tile_map, seed

# Generate a random tile map with a random seed (or specify a seed)
input_seed = None  # Set to None for random seed, or specify an integer for a specific seed
TILE_MAP_WIDTH, TILE_MAP_HEIGHT = 20, 20  # Increase the map size for more variation
tile_map, seed = generate_random_tile_map(TILE_MAP_WIDTH, TILE_MAP_HEIGHT, input_seed)

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

    # Calculate the offset for the top-left corner of the visible area in the tile map
    offset_x = camera_x // TILE_SIZE
    offset_y = camera_y // TILE_SIZE

    # Draw the tiles
    for y in range(-1, SCREEN_HEIGHT // TILE_SIZE + 2):
        for x in range(-1, SCREEN_WIDTH // TILE_SIZE + 2):
            map_x = (x + offset_x) % TILE_MAP_WIDTH
            map_y = (y + offset_y) % TILE_MAP_HEIGHT
            tile_type = tile_map[map_y][map_x]
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
