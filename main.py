import math
import pygame
import sys
import random
from base_enemy import Enemy, enemies
from crashing_enemy import crashingEnemy, crashing_enemies

# Initialize Pygame
pygame.init()

# Set up the game window
fullscreen = False  # Change this variable to switch between fullscreen and windowed mode
menu_font = pygame.font.Font(None, 36)

if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen_width = 690  # Screen width
    screen_height = 690  # Screen height
    screen = pygame.display.set_mode((screen_width, screen_height))

width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("2D Shooter")
FPS = 60

tile_image = pygame.image.load('sprites/tile.png')
tile_size = 128  # Desired display size of each tile
scaled_tile_image = pygame.transform.scale(tile_image, (tile_size, tile_size))  # Scale the image

# Load sprite sheet for the character walking
sprite_sheet_path_right = 'sprites/Niko_right.png'
sprite_sheet_path_up = 'sprites/Niko_up.png'
sprite_sheet_path_down = 'sprites/Niko_down.png'
sprite_sheet_path_left = 'sprites/Niko_left.png'
sprite_sheet_right = pygame.image.load(sprite_sheet_path_right).convert_alpha()
sprite_sheet_up = pygame.image.load(sprite_sheet_path_up).convert_alpha()
sprite_sheet_down = pygame.image.load(sprite_sheet_path_down).convert_alpha()
sprite_sheet_left = pygame.image.load(sprite_sheet_path_left).convert_alpha()

# Frame setup
frame_width, frame_height = 24, 30
scaling_factor = 2.77
niko_scaling_width, niko_scaling_height = frame_width * scaling_factor, frame_height * scaling_factor
frames_up = [pygame.transform.scale(sprite_sheet_up.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (niko_scaling_width, niko_scaling_height)) for i in range(3)]
frames_right = [pygame.transform.scale(sprite_sheet_right.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (niko_scaling_width, niko_scaling_height)) for i in range(3)]
frames_down = [pygame.transform.scale(sprite_sheet_down.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (niko_scaling_width, niko_scaling_height)) for i in range(3)]
frames_left = [pygame.transform.scale(sprite_sheet_left.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (niko_scaling_width, niko_scaling_height)) for i in range(3)]
current_frame = 0
frame_count = 0
rendering = "down"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player attributes
player_x = width // 2
player_y = height // 2
player_speed = 5
player_height = frame_width
player_width = frame_height
player_hp = 100
invince_frames = 10
i_frame_temp = invince_frames
kills = 0

# Experience system
exp = 0
enemy_exp = 0
active_exp_orbs = []
current_max_exp = 30
max_level = 1000  # for ending
player_level = 1  # keeping track of the player's current level
exp_increase_per_level = 5
levelling = False

# Bullet attributes
bullets = []
bullet_speed = 10
bullet_frames = []
for i in range(1, 6):  # Assume there are five fireball images named fireball1.png to fireball5.png
    original_frame = pygame.image.load(f"sprites/fireball{i}.png").convert_alpha()
    scaled_width = original_frame.get_width() * 2
    scaled_height = original_frame.get_height() * 2
    scaled_frame = pygame.transform.scale(original_frame, (scaled_width, scaled_height))
    bullet_frames.append(scaled_frame)

base_enemy_exp = random.randint(1, 5)
ENEMY_SPEED = 0.5  # Adjust this value as needed

# Load experience orb image
exp_image = pygame.image.load("sprites/exp.png")

paused = False

# Gun variables
base_gun_cooldown = 2
base_sword_cooldown = 1

def draw_tiles(camera_offset_x, camera_offset_y):
    for y in range(-tile_size, height + tile_size, tile_size):
        for x in range(-tile_size, width + tile_size, tile_size):
            screen.blit(scaled_tile_image, (x + camera_offset_x % tile_size - tile_size, y + camera_offset_y % tile_size - tile_size))

def animate_bullet(bullet):
    bullet['frame'] += 1
    if bullet['frame'] >= len(bullet_frames):
        bullet['frame'] = 0
    return bullet_frames[bullet['frame']]

def shoot_base_gun(player_x, player_y, bullets, bullet_speed):
    mouseX, mouseY = pygame.mouse.get_pos()
    angle = math.atan2(mouseY - height // 2, mouseX - width // 2)  # Use the center of the screen for angle calculation
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(angle),
        'dy': bullet_speed * math.sin(angle),
        'frame': 0  # Start animation frame
    })

def draw_kill_counter(kills):
    font = pygame.font.Font(None, 24)
    kills_text = font.render(f"Kills: {kills}", True, RED)
    text_width, text_height = font.size(f"Kills: {kills}")
    text_x = (width - text_width) // 3
    text_y = 20
    screen.blit(kills_text, (text_x, text_y))

# level up function
def level_up():
    global player_level, exp, current_max_exp, paused  # Declare global variables
    player_level += 1
    exp -= current_max_exp  # Subtract current max exp from player's exp
    current_max_exp = int(current_max_exp * 1.2)  # Increase current max exp exponentially for the next level
    paused = True

# Function to draw experience bar
def draw_exp_bar():
    max_exp = current_max_exp
    exp_bar_width = width - 20  # Define the width of the experience bar
    exp_bar_height = 20
    exp_indicator_width = int(exp / max_exp * exp_bar_width)  # Calculate the width of the experience indicator

    pygame.draw.rect(screen, BLUE, (10, 10, exp_bar_width, exp_bar_height))  # Blue background
    pygame.draw.rect(screen, GREEN, (10, 10, exp_indicator_width, exp_bar_height))  # Green indicator

    font = pygame.font.Font(None, 24)
    exp_text = font.render(f"EXP: {exp}/{max_exp}", True, WHITE)
    text_width, text_height = font.size(f"EXP: {exp}/{max_exp}")
    text_x = (width - text_width) // 2
    text_y = exp_bar_height + 20
    screen.blit(exp_text, (text_x, text_y))

# Function to spawn enemies
def spawn_enemy(player_x, player_y):
    enemy_x = random.randint(-width // 2, width // 2) + player_x
    enemy_y = random.randint(-height // 2, height // 2) + player_y

    basic_enemy = Enemy(enemy_x, enemy_y, 20, 20, 10, ENEMY_SPEED)
    enemies.append(basic_enemy)

# Function to spawn crashing enemies
def spawn_crashing_enemy(player_x, player_y):
    enemy_x = random.randint(-width // 2, width // 2) + player_x
    enemy_y = random.randint(-height // 2, height // 2) + player_y

    crashingenemy = crashingEnemy(enemy_x, enemy_y, 20, 20, 10, ENEMY_SPEED)
    crashing_enemies.append(crashingenemy)

# Function to draw player's health bar
def draw_hp_bar():
    hp_bar_width = player_hp * 2
    hp_bar_height = 20
    hp_indicator_width = int(player_hp / 100 * hp_bar_width)

    pygame.draw.rect(screen, RED, (10, height - 30, hp_bar_width, hp_bar_height))  # Red background
    pygame.draw.rect(screen, GREEN, (10, height - 30, hp_indicator_width, hp_bar_height))  # Green indicator
    font = pygame.font.Font(None, 36)
    hp_text = font.render(f"{player_hp}/100 HP", True, WHITE)
    screen.blit(hp_text, (220, height - 30))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused  # Toggle pause state

        if pygame.mouse.get_pressed()[0] and paused is False:
            shoot_base_gun(player_x, player_y, bullets, bullet_speed)

    if not paused:  # Only update game state if not paused
        # Update player input and game state
        player_rect = pygame.Rect(player_x, player_y, niko_scaling_width, niko_scaling_height)
        keys = pygame.key.get_pressed()

        # Calculate movement vector
        move_x, move_y = 0, 0
        if keys[pygame.K_a]:
            move_x -= player_speed
            rendering = "left"
        if keys[pygame.K_d]:
            move_x += player_speed
            rendering = "right"
        if keys[pygame.K_w]:
            move_y -= player_speed
            rendering = "up"
        if keys[pygame.K_s]:
            move_y += player_speed
            rendering = "down"

        # Normalize the movement vector to prevent faster diagonal movement
        if move_x != 0 and move_y != 0:
            move_x *= math.sqrt(0.5)
            move_y *= math.sqrt(0.5)

        # Update player position
        player_x += move_x
        player_y += move_y

        # Update frame count and current frame if the player is moving
        if move_x != 0 or move_y != 0:
            frame_count += 1
            if frame_count % 2 == 0:  # Adjust frame rate of animation here
                current_frame = (current_frame + 1) % 3  # Assuming each direction has 3 frames

        # Update bullet positions and animate
        for bullet in bullets:
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            bullet_image = animate_bullet(bullet)  # Animate bullet
            angle = math.atan2(-bullet['dy'], bullet['dx'])  # Calculate angle for rotation
            rotated_bullet_image = pygame.transform.rotate(bullet_image, math.degrees(angle))
            screen.blit(rotated_bullet_image, (bullet['x'] - rotated_bullet_image.get_width() / 2, bullet['y'] - rotated_bullet_image.get_height() / 2))

        # Filter bullets that go off-screen
        bullets = [bullet for bullet in bullets if bullet['x'] > player_x - width // 2 and bullet['x'] < player_x + width // 2 and bullet['y'] > player_y - height // 2 and bullet['y'] < player_y + height // 2]

        # Spawn new enemies randomly
        if random.randint(0, 100) < 5:
            spawn_enemy(player_x, player_y)
        elif random.randint(0, 1000) == 69:
            spawn_crashing_enemy(player_x, player_y)

        # Update enemy positions and check for collisions with the player
        for crashing_enemy in crashing_enemies:
            distance_y = player_y - crashing_enemy.y  # Calculate the vertical distance between player and enemy
            distance_x = player_x - crashing_enemy.x  # Calculate the horizontal distance between player and enemy

            # Calculate the angle between the player and the enemy
            angle = math.atan2(distance_y, distance_x)

            # Calculate the movement components based on the angle and enemy speed
            move_x = ENEMY_SPEED * math.cos(angle)
            move_y = ENEMY_SPEED * math.sin(angle)

            # Update enemy position
            crashing_enemy.x += move_x
            crashing_enemy.y += move_y

            if player_rect.colliderect(crashing_enemy.rect):  # Use rect attribute of enemies
                if invince_frames == i_frame_temp:
                    player_hp -= 5
                    invince_frames = 0

            # Check for collisions with bullets
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet['x'] - 5, bullet['y'] - 5, 10, 10)
                enemy_rect = pygame.Rect(crashing_enemy.x, crashing_enemy.y, crashing_enemy.width, crashing_enemy.height)

                if bullet_rect.colliderect(enemy_rect):
                    crashing_enemy.hp -= 10
                    bullets.remove(bullet)

                    if crashing_enemy.hp <= 0:
                        sys.exit()

        for enemy in enemies:
            distance_y = player_y - enemy.y  # Calculate the vertical distance between player and enemy
            distance_x = player_x - enemy.x  # Calculate the horizontal distance between player and enemy

            # Calculate the angle between the player and the enemy
            angle = math.atan2(distance_y, distance_x)

            # Calculate the movement components based on the angle and enemy speed
            move_x = ENEMY_SPEED * math.cos(angle)
            move_y = ENEMY_SPEED * math.sin(angle)

            # Update enemy position
            enemy.x += move_x
            enemy.y += move_y

            # Check for collisions with the player
            if (player_x < enemy.x + enemy.width and player_x + player_width > enemy.x and
                    player_y < enemy.y + enemy.height and player_y + player_height > enemy.y):
                if invince_frames == i_frame_temp:
                    player_hp -= 5
                    invince_frames = 0

            # Check for collisions with bullets
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet['x'] - 5, bullet['y'] - 5, 10, 10)
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

                if bullet_rect.colliderect(enemy_rect):
                    enemy.hp -= 10
                    bullets.remove(bullet)

                    if enemy.hp <= 0:
                        enemies.remove(enemy)
                        active_exp_orbs.append({'size': enemy_exp * 3, 'x': enemy.x, 'y': enemy.y, 'value': enemy_exp})
                        enemy_exp = random.randint(1, 5)
                        kills += 1

        if player_hp <= 0:
            sys.exit()

        # Check for collisions between player and exp orbs
        for exp_orb in active_exp_orbs:
            orb_center_x = exp_orb['x']
            orb_center_y = exp_orb['y']
            orb_radius = exp_orb['size']
            orb_exp = exp_orb['value']  # Extract the exp value associated with the orb

            # Calculate the distance between player and exp orb's center
            distance_to_orb = math.sqrt((player_x - orb_center_x) ** 2 + (player_y - orb_center_y) ** 2)

            # Check if the player collides with the exp orb
            if distance_to_orb < orb_radius + player_width / 2:
                # Player gains exp equal to the amount associated with the exp orb
                exp += orb_exp
                # Remove the exp orb from the active list
                active_exp_orbs.remove(exp_orb)

    # Calculate camera offset
    camera_offset_x = width // 2 - player_x
    camera_offset_y = height // 2 - player_y

    # Draw elements
    screen.fill(BLACK)  # Clear the screen
    draw_tiles(camera_offset_x, camera_offset_y)

    # Draw player, enemies, bullets, health bar, and experience bar...
    for exp_orb in active_exp_orbs:
        # Calculate the top-left corner of the image so it's centered on the orb's position
        image_x = exp_orb['x'] - exp_image.get_width() // 2 + camera_offset_x
        image_y = exp_orb['y'] - exp_image.get_height() // 2 + camera_offset_y
        screen.blit(exp_image, (image_x, image_y))

    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy.x + camera_offset_x, enemy.y + camera_offset_y, enemy.width, enemy.height))

    for crashing_enemy in crashing_enemies:
        pygame.draw.rect(screen, BLUE, (crashing_enemy.x + camera_offset_x, crashing_enemy.y + camera_offset_y, crashing_enemy.width, crashing_enemy.height))

    for bullet in bullets:
        # Calculate angle of rotation based on bullet's velocity
        angle = math.atan2(-bullet['dy'], bullet['dx'])  # Use negative y-velocity to account for inverted y-axis

        # Rotate the bullet image
        rotated_bullet_image = pygame.transform.rotate(bullet_image, math.degrees(angle))

        # Draw the rotated bullet image at the bullet's position
        screen.blit(rotated_bullet_image, (
            bullet['x'] - rotated_bullet_image.get_width() / 2 + camera_offset_x, bullet['y'] - rotated_bullet_image.get_height() / 2 + camera_offset_y))

    draw_hp_bar()  # Draw the player's HP bar
    draw_exp_bar()  # Draw the experience bar
    draw_kill_counter(kills)
    if rendering == "right":
        screen.blit(frames_right[current_frame], (width // 2, height // 2))  # Draw the current frame of player sprite
    if rendering == "up":
        screen.blit(frames_up[current_frame], (width // 2, height // 2))
    if rendering == "left":
        screen.blit(frames_left[current_frame], (width // 2, height // 2))
    if rendering == "down":
        screen.blit(frames_down[current_frame], (width // 2, height // 2))
    if invince_frames < i_frame_temp:
        invince_frames += 1
    if exp >= current_max_exp:
        level_up()

    # If game is paused, show pause menu
    if paused:
        pause_text = menu_font.render("PAUSED", True, WHITE)
        text_width, text_height = menu_font.size("PAUSED")
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2
        screen.blit(pause_text, (text_x, text_y))

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)
