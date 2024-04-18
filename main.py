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

if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen_width = 690  # Set your desired window width
    screen_height = 690  # Set your desired window height
    screen = pygame.display.set_mode((screen_width, screen_height))

width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("2D Shooter")

tile_image = pygame.image.load('sprites/tile.png')
original_tile_size = 476  # Original size of the tile image
tile_size = 64  # Desired display size of each tile
scaled_tile_image = pygame.transform.scale(tile_image, (tile_size, tile_size))  # Scale the image

# Load sprite sheet for the character walking to the right
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
frames_up = [pygame.transform.scale(sprite_sheet_up.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (48, 60)) for i in range(3)]
frames_right = [pygame.transform.scale(sprite_sheet_right.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (48, 60)) for i in range(3)]
frames_down = [pygame.transform.scale(sprite_sheet_down.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (48, 60)) for i in range(3)]
frames_left = [pygame.transform.scale(sprite_sheet_left.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (48, 60)) for i in range(3)]
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

# Recoil attributes
recoil_strength = 0  # Adjust this value to control the strength of the recoil
recoil_duration = 0  # Adjust this value to control how long the recoil effect lasts
recoil_counter = 0

base_enemy_exp = random.randint(1, 5)

ENEMY_SPEED = 0.5  # Adjust this value as needed

paused = False

def draw_tiles():
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            screen.blit(scaled_tile_image, (x, y))

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
def spawn_enemy():
    spawn_side = random.randint(0, 3)
    if spawn_side == 0:
        enemy_x = random.randint(0, width)
        enemy_y = height + 20
    elif spawn_side == 1:
        enemy_x = random.randint(0, width)
        enemy_y = -height - 20
    elif spawn_side == 2:
        enemy_x = -width - 20
        enemy_y = random.randint(0, height)
    else:
        enemy_x = width + 20
        enemy_y = random.randint(0, height)

    basic_enemy = Enemy(enemy_x, enemy_y, 20, 20, 10, ENEMY_SPEED)
    enemies.append(basic_enemy)


# Function to spawn enemies
def spawn_crashing_enemy():
    spawn_side = random.randint(0, 3)
    if spawn_side == 0:
        enemy_x = random.randint(0, width)
        enemy_y = height + 20
    elif spawn_side == 1:
        enemy_x = random.randint(0, width)
        enemy_y = -height - 20
    elif spawn_side == 2:
        enemy_x = -width - 20
        enemy_y = random.randint(0, height)
    else:
        enemy_x = width + 20
        enemy_y = random.randint(0, height)
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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseX, mouseY = pygame.mouse.get_pos()
            angle = math.atan2(mouseY - player_y, mouseX - player_x)
            bullets.append([player_x, player_y, bullet_speed * math.cos(angle), bullet_speed * math.sin(angle)])

            # Apply recoil when shooting
            player_x -= recoil_strength * math.cos(angle)
            player_y -= recoil_strength * math.sin(angle)

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        paused = True

    if not paused:  # Only update game state if not paused
        # Update player input and game state
        global crashing_enemy
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= player_speed
            frame_count += 1
            if frame_count % 2 == 0:  # Adjust frame rate of animation here
                current_frame = (current_frame + 1) % len(frames_left)
            rendering = "left"
        if keys[pygame.K_d]:
            player_x += player_speed
            frame_count += 1
            if frame_count % 2 == 0:  # Adjust frame rate of animation here
                current_frame = (current_frame + 1) % len(frames_right)
            rendering = "right"
        if keys[pygame.K_w]:
            player_y -= player_speed
            frame_count += 1
            if frame_count % 2 == 0:
                current_frame = (current_frame + 1) % len(frames_up)
            rendering = "up"
        if keys[pygame.K_s]:
            player_y += player_speed
            frame_count += 1
            if frame_count % 2 == 0:  # Adjust frame rate of animation here
                current_frame = (current_frame + 1) % len(frames_down)
            rendering = "down"

        # Update bullet positions and remove bullets that go off-screen
        for bullet in bullets:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]

        bullets = [bullet for bullet in bullets if 0 <= bullet[0] <= width and 0 <= bullet[1] <= height]

        # Spawn new enemies randomly
        if random.randint(0, 100) < 5:
            spawn_enemy()

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

            # Check for collisions with the player
            if (player_x < crashing_enemy.x + crashing_enemy.width and player_x + player_width > crashing_enemy.x and
                    player_y < crashing_enemy.y + crashing_enemy.height and player_y + player_height > crashing_enemy.y):
                if invince_frames == i_frame_temp:
                    player_hp -= 5
                    invince_frames = 0

            # Check for collisions with bullets
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet[0] - 5, bullet[1] - 5, 10, 10)
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
                bullet_rect = pygame.Rect(bullet[0] - 5, bullet[1] - 5, 10, 10)
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

                if bullet_rect.colliderect(enemy_rect):
                    enemy.hp -= 10
                    bullets.remove(bullet)

                    if enemy.hp <= 0:
                        enemies.remove(enemy)
                        active_exp_orbs.append({'size': enemy_exp * 3, 'x': enemy.x, 'y': enemy.y, 'value': enemy_exp})
                        enemy_exp = random.randint(1, 5)

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

    # Add code to handle pausing the game
    if paused:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            paused = False

        pygame.time.Clock().tick(60)  # Limit frame rate to reduce CPU usage

    # Draw elements
    screen.fill(BLACK)  # Clear the screen
    draw_tiles()

    # Draw player, enemies, bullets, health bar, and experience bar...
    for exp_orb in active_exp_orbs:
        pygame.draw.circle(screen, GREEN, (exp_orb['x'], exp_orb['y']), exp_orb['size'] + 1)  # Exp orbs

    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy.x, enemy.y, enemy.width, enemy.height))  # Enemies

    for crashing_enemy in crashing_enemies:
        pygame.draw.rect(screen, BLUE, (crashing_enemy.x, crashing_enemy.y, crashing_enemy.width, crashing_enemy.height))

    for bullet in bullets:
        pygame.draw.circle(screen, GREEN, (int(bullet[0]), int(bullet[1])), 5)  # Bullets

    draw_hp_bar()  # Draw the player's HP bar
    draw_exp_bar()  # Draw the experience bar
    screen.blit(frames_down[current_frame], (player_x, player_y))
    if rendering == "right":
        screen.blit(frames_right[current_frame], (player_x, player_y))  # Draw the current frame of player sprite
    if rendering == "up":
        screen.blit(frames_up[current_frame], (player_x, player_y))
    if rendering == "left":
        screen.blit(frames_left[current_frame], (player_x, player_y))
    if rendering == "down":
        screen.blit(frames_down[current_frame], (player_x, player_y))
    if invince_frames < i_frame_temp:
        invince_frames += 1
    if exp >= current_max_exp:
        level_up()

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)
