import math
import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

# Set up the game window
fullscreen = False
if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen_width = 690
    screen_height = 690
    screen = pygame.display.set_mode((screen_width, screen_height))

width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("Main Menu")

FPS = 60
clock = pygame.time.Clock()

# Load assets
tile_image = pygame.image.load('../sprites/tile.png')
tile_size = 128
scaled_tile_image = pygame.transform.scale(tile_image, (tile_size, tile_size))
cursor_image = pygame.image.load("../sprites/cursor.png")

play_button_image = pygame.image.load('../sprites/play.png')
settings_button_image = pygame.image.load('../sprites/settings.png')
quit_button_image = pygame.image.load('../sprites/quit.png')

# Button positions
play_button_rect = play_button_image.get_rect(center=(width // 4, height // 2))
settings_button_rect = settings_button_image.get_rect(center=(width // 2, height - 50))
quit_button_rect = quit_button_image.get_rect(center=(3 * width // 4, height // 2))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player attributes
player_pos_on_screen = (width // 2, height // 2)
player_x = width // 2
player_y = height // 2
player_speed = 5
player_height = 60
player_width = 60

# Load sprite for the character looking down
sprite_sheet_path_down = '../sprites/Niko_down.png'
sprite_sheet_down = pygame.image.load(sprite_sheet_path_down).convert_alpha()

frame_width, frame_height = 24, 30
scaling_factor = 2.77
niko_scaling_width, niko_scaling_height = frame_width * scaling_factor, frame_height * scaling_factor
frames_down = [pygame.transform.scale(sprite_sheet_down.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (niko_scaling_width, niko_scaling_height)) for i in range(3)]
current_frame = 0
frame_count = 0

# Bullet attributes
bullets = []
bullet_speed = 10
bullet_frames = []
for i in range(1, 6):  # Assume there are five fireball images named fireball1.png to fireball5.png
    bullet_original_frame = pygame.image.load(f"sprites/fireball{i}.png").convert_alpha()
    bullet_scaled_width = bullet_original_frame.get_width() * 2
    bullet_scaled_height = bullet_original_frame.get_height() * 2
    bullet_scaled_frame = pygame.transform.scale(bullet_original_frame, (bullet_scaled_width, bullet_scaled_height))
    bullet_frames.append(bullet_scaled_frame)

fireball_cooldown = 50  # Cooldown period in frames
current_fireball_cooldown = 0  # Tracks the current cooldown state

def draw_tiles():
    for y in range(-tile_size, height + tile_size, tile_size):
        for x in range(-tile_size, width + tile_size, tile_size):
            screen.blit(scaled_tile_image, (x, y))

def animate_bullet(bullet):
    bullet['frame'] += 1
    if bullet['frame'] >= len(bullet_frames):
        bullet['frame'] = 0
    return bullet_frames[bullet['frame']]

def shoot_bullet(player_x, player_y, bullet_speed, angle, bullets):
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(angle),
        'dy': bullet_speed * math.sin(angle),
        'frame': 0
    })

def handle_bullet_collisions(bullets, target_rect, action):
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet['x'] - 10, bullet['y'] - 10, 20, 20)
        if bullet_rect.colliderect(target_rect):
            action()

def start_game():
    print("Starting game...")
    # Logic to transition to the main game

def open_settings():
    print("Opening settings...")
    # Logic to open settings menu

def quit_game():
    print("Quitting game...")
    pygame.quit()
    sys.exit()

while True:
    cursor_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    move_x, move_y = 0, 0
    if keys[pygame.K_a]:
        move_x -= player_speed
    if keys[pygame.K_d]:
        move_x += player_speed
    if keys[pygame.K_w]:
        move_y -= player_speed
    if keys[pygame.K_s]:
        move_y += player_speed

    if move_x != 0 and move_y != 0:
        move_x *= math.sqrt(0.5)
        move_y *= math.sqrt(0.5)

    player_x += move_x
    player_y += move_y

    if pygame.mouse.get_pressed()[0] and current_fireball_cooldown == 0:
        centered_x, centered_y = player_x + player_width // 2, player_y + player_height // 4
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - centered_y, mouse_x - centered_x)
        shoot_bullet(centered_x, centered_y, bullet_speed, angle, bullets)
        current_fireball_cooldown = fireball_cooldown  # Reset the cooldown

    if current_fireball_cooldown > 0:
        current_fireball_cooldown -= 1

    screen.fill(BLACK)
    draw_tiles()
    screen.blit(play_button_image, play_button_rect.topleft)
    screen.blit(settings_button_image, settings_button_rect.topleft)
    screen.blit(quit_button_image, quit_button_rect.topleft)

    bullets = [bullet for bullet in bullets if 0 <= bullet['x'] <= width and 0 <= bullet['y'] <= height]
    for bullet in bullets:
        bullet['x'] += bullet['dx']
        bullet['y'] += bullet['dy']
        bullet_image = animate_bullet(bullet)
        angle = math.atan2(-bullet['dy'], bullet['dx'])
        rotated_bullet_image = pygame.transform.rotate(bullet_image, math.degrees(angle))
        screen.blit(rotated_bullet_image, (bullet['x'] - rotated_bullet_image.get_width() / 2, bullet['y'] - rotated_bullet_image.get_height() / 2))

    handle_bullet_collisions(bullets, play_button_rect, start_game)
    handle_bullet_collisions(bullets, settings_button_rect, open_settings)
    handle_bullet_collisions(bullets, quit_button_rect, quit_game)



    screen.blit(frames_down[current_frame], player_pos_on_screen)  # Always render the player looking down

    screen.blit(cursor_image, cursor_pos)
    pygame.display.flip()
    clock.tick(FPS)
