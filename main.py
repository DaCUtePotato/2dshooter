import math
import pygame
import sys
import random
from base_enemy import Enemy, enemies
from crashing_enemy import crashingEnemy, crashing_enemies

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

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
clock = pygame.time.Clock()
running = True

tile_image = pygame.image.load('sprites/tile.png')  # Load tiles for the game
tile_size = 128  # Desired display size of each tile
scaled_tile_image = pygame.transform.scale(tile_image, (tile_size, tile_size))  # Scale the image
cursor_image = pygame.image.load("sprites/cursor.png")
play_button_image = pygame.image.load('sprites/play.png')
settings_button_image = pygame.image.load('sprites/settings.png')
quit_button_image = pygame.image.load('sprites/quit.png')

# Button positions
play_button_rect = play_button_image.get_rect(center=(width // 4, height // 2))
settings_button_rect = settings_button_image.get_rect(center=(width // 2, height - 50))
quit_button_rect = quit_button_image.get_rect(center=(3 * width // 4, height // 2))

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
player_pos_on_screen = (width // 2, height // 2)
player_x = width//2
player_y = height // 2
hyp_player_x = player_x
hyp_player_y = player_y
player_speed = 5
player_height = int(niko_scaling_height)
player_width = int(niko_scaling_width)
player_hp = 100
invince_frames = 10
i_frame_temp = invince_frames
kills = 0

# Correctly position the hitbox at the center of the player sprite
player_hitbox = pygame.Rect(player_x - player_width // 2, player_y - player_height // 2, player_width-3, player_height-3)
center_x = player_x + player_width / 2
center_y = player_y + player_height / 4

# Experience system
gambling_mode = False
exp = 0
enemy_exp = random.randint(1, 5)
active_exp_orbs = []
current_max_exp = 30
max_level = 10000  # for ending
player_level = 1  # keeping track of the player's current level
exp_increase_per_level = 5
levelling = False
pickup_sound = pygame.mixer.Sound("sounds/exp.wav")
level_up_sound = pygame.mixer.Sound("sounds/level_up_normal.wav")
gambling_sound = pygame.mixer.Sound("sounds/gambling.wav")

#Regeneration
active_regen_orbs = []
regen_amount = 30
pickup_sound_regen = pygame.mixer.Sound("sounds/pickup_regen.wav")
regen_orb_size = 15

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

ENEMY_SPEED = 0.5  # Adjust this value as needed
enemy_frames = []
for i in range(1, 4):  # Assuming there are 3 enemy images named enemy1.png, enemy2.png, and enemy3.png
    enemy_original_frame = pygame.image.load(f"sprites/enemies/enemy{i}.png").convert_alpha()
    enemy_scaled_width = enemy_original_frame.get_width() * 5  # Adjust the scaling factor as needed
    enemy_scaled_height = enemy_original_frame.get_height() * 5
    enemy_scaled_frame = pygame.transform.scale(enemy_original_frame, (enemy_scaled_width, enemy_scaled_height))
    enemy_frames.append(enemy_scaled_frame)

# Load experience orb image
exp_image = pygame.image.load("sprites/exp.png")

# Load regen orb image
regen_image = pygame.image.load("sprites/regen_orb.png")

paused = False

# Fireball variables
fireball_sound_1 = pygame.mixer.Sound("sounds/fireball1.wav")
fireball_sound_2 = pygame.mixer.Sound("sounds/fireball2.wav")
fireball_sound_3 = pygame.mixer.Sound("sounds/fireball3.wav")
fireball_sound_4 = pygame.mixer.Sound("sounds/fireball4.wav")
fireball_sound_5 = pygame.mixer.Sound("sounds/fireball5.wav")
fireball_sound_6 = pygame.mixer.Sound("sounds/fireball6.wav")
fireball_sound_7 = pygame.mixer.Sound("sounds/fireball7.wav")
base_fireball_cooldown = 50
current_fireball_cooldown = 0
upgrades = 0

cooldown_reduction_upgrade1 = 10 # Cooldown reduction Upgrade 1
cooldown_reduction_upgrade2 = 5 # Cooldown reduction Upgrade 2
cooldown_reduction_upgrade3 = 10 # Cooldown reduction Upgrade 3
cooldown_reduction_upgrade4 = 5 # Same here
cooldown_reduction_upgrade5 = 5
cooldown_reduction_upgrade6 = -40
cooldown_reduction_upgrade7 = 10

def draw_tiles(camera_offset_x, camera_offset_y):
    for y in range(-tile_size, height + tile_size, tile_size):
        for x in range(-tile_size, width + tile_size, tile_size):
            screen.blit(scaled_tile_image, (x + camera_offset_x % tile_size - tile_size, y + camera_offset_y % tile_size - tile_size))

def animate_bullet(bullet):
    bullet['frame'] += 1
    if bullet['frame'] >= len(bullet_frames):
        bullet['frame'] = 0
    return bullet_frames[bullet['frame']]

def shoot_forwards(player_x, player_y,bullet_speed,angle, bullets):
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(angle),
        'dy': bullet_speed * math.sin(angle),
        'frame': 0  # Start animation frame
    })
def shoot_backwards(player_x, player_y,bullet_speed, angle, bullets):
    # Shoot fireball in the opposite direction
    backwards_angle = angle + math.pi  # Calculate opposite angle
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(backwards_angle),
        'dy': bullet_speed * math.sin(backwards_angle),
        'frame': 0  # Start animation frame
    })

def shoot_right(player_x, player_y,bullet_speed, angle, bullets):
    # Shoot fireball to the right
    right_angle = angle + math.pi / 2  # Angle for right direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(right_angle),
        'dy': bullet_speed * math.sin(right_angle),
        'frame': 0  # Start animation frame
    })

def shoot_left(player_x, player_y,bullet_speed, angle, bullets):
    # Shoot fireball to the left
    left_angle = angle - math.pi / 2  # Angle for left direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(left_angle),
        'dy': bullet_speed * math.sin(left_angle),
        'frame': 0  # Start animation frame
    })

def shoot_up_directional(player_x, player_y,bullet_speed, angle, bullets):
    upright_angle = angle + math.pi / 4  # Angle for upright direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(upright_angle),
        'dy': bullet_speed * math.sin(upright_angle),
        'frame': 0  # Start animation frame
    })
    # Shoot fireball upleft
    upleft_angle = angle - math.pi / 4  # Angle for upleft direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(upleft_angle),
        'dy': bullet_speed * math.sin(upleft_angle),
        'frame': 0  # Start animation frame
    })

def shoot_down_directional(player_x, player_y,bullet_speed, angle, bullets):
    downright_angle = angle + 3 * math.pi / 4  # Angle for upright direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(downright_angle),
        'dy': bullet_speed * math.sin(downright_angle),
        'frame': 0  # Start animation frame
    })
    # Shoot fireball upleft
    downleft_angle = angle - 3 * math.pi / 4  # Angle for upleft direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(downleft_angle),
        'dy': bullet_speed * math.sin(downleft_angle),
        'frame': 0  # Start animation frame
    })

def shoot_base_fireball(player_x, player_y, bullets, bullet_speed):
    global current_fireball_cooldown
    centered_x, centered_y = player_x+player_width//2, player_y+player_height//4
    mouseX, mouseY = pygame.mouse.get_pos()
    angle = math.atan2(mouseY-height//2-player_height//4, mouseX-width//2-player_width//2)  # Use the center of the screen for angle calculation
    if upgrades == 7:  # If the 7th upgrade is active, shoot upwards
        up = -math.pi / 2  # Angle for shooting upwards
        shoot_forwards(centered_x, centered_y, bullet_speed, up, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, up, bullets)
        shoot_right(centered_x, centered_y, bullet_speed, up, bullets)
        shoot_left(centered_x, centered_y, bullet_speed, up, bullets)
        shoot_up_directional(centered_x, centered_y, bullet_speed, up, bullets)
        shoot_down_directional(centered_x, centered_y, bullet_speed, up, bullets)
        fireball_sound_7.play()

    if upgrades == 0:
        shoot_forwards(centered_x, centered_y, bullet_speed,angle, bullets)
        fireball_sound_1.set_volume(0.5)  # Set volume to 50%
        fireball_sound_1.play()
    elif upgrades == 1:
        fireball_sound_2.play()
        shoot_forwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, angle, bullets)
    elif upgrades == 2:
        fireball_sound_3.play()
        shoot_forwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_right(centered_x, centered_y, bullet_speed, angle, bullets)
    elif upgrades == 3:
        fireball_sound_4.play()
        shoot_forwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_right(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_left(centered_x, centered_y, bullet_speed, angle, bullets)
    elif upgrades == 4:
        fireball_sound_5.play()
        shoot_forwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_right(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_left(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_up_directional(centered_x, centered_y, bullet_speed, angle, bullets)
    elif upgrades == 5 or upgrades==6:
        fireball_sound_6.play()
        shoot_forwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_right(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_left(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_up_directional(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_down_directional(centered_x, centered_y, bullet_speed, angle, bullets)

    # Apply the reduced cooldown based on the upgrades
    cooldown_reduction = 0
    if upgrades == 1:
        cooldown_reduction += cooldown_reduction_upgrade1
    if upgrades == 2:
        cooldown_reduction += cooldown_reduction_upgrade2
    if upgrades == 3:
        cooldown_reduction += cooldown_reduction_upgrade3
    if upgrades == 4:
        cooldown_reduction += cooldown_reduction_upgrade4
    if upgrades == 5:
        cooldown_reduction += cooldown_reduction_upgrade5
    if upgrades == 6:
        cooldown_reduction += cooldown_reduction_upgrade6
    if upgrades == 7:
        cooldown_reduction += cooldown_reduction_upgrade7
    current_fireball_cooldown = base_fireball_cooldown - cooldown_reduction  # Apply reduced cooldown

def draw_kill_counter(kills):
    font = pygame.font.Font(None, 24)
    kills_text = font.render(f"Kills: {kills}", True, RED)
    text_width, text_height = font.size(f"Kills: {kills}")
    text_x = (width - text_width) // 3
    text_y = 20
    screen.blit(kills_text, (text_x, text_y))

def draw_coordinates(player_x, player_y):
    font = pygame.font.Font(None, 24)
    coordinate_text = font.render(f"Coordinates: {int(player_x)}:{int(player_y)}", True, WHITE)
    text_width, text_height = font.size(f"Coordinates: {coordinate_text}")
    text_x = (width - text_width)
    text_y = 20
    screen.blit(coordinate_text, (text_x, text_y))

# level up function
def level_up():
    global player_level, exp, current_max_exp, paused, show_upgrade_menu  # Declare global variables
    player_level += 1
    exp -= current_max_exp  # Subtract current max exp from player's exp
    current_max_exp = int(current_max_exp * 1.3)  # Increase current max exp exponentially for the next level
    paused = True
    show_upgrade_menu = True  # Show the upgrade menu
    if gambling_mode:
        gambling_sound.play()
    elif gambling_mode == False:
        level_up_sound.play()

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
    # Calculate the boundaries for off-screen spawning
    off_screen_buffer = 10  # Distance outside the screen to ensure spawning off-screen
    spawn_x = player_x + random.choice([-1, 1]) * (random.randint(screen_width // 2 + off_screen_buffer, screen_width))
    spawn_y = player_y + random.choice([-1, 1]) * (random.randint(screen_height // 2 + off_screen_buffer, screen_height))

    basic_enemy = Enemy(spawn_x, spawn_y, enemy_scaled_width, enemy_scaled_height, 10, ENEMY_SPEED)
    enemies.append(basic_enemy)

# Function to spawn crashing enemies
def spawn_crashing_enemy(player_x, player_y):
    off_screen_buffer = 10  # Distance outside the screen to ensure spawning off-screen
    spawn_x = player_x + random.choice([-1, 1]) * (random.randint(screen_width // 2 + off_screen_buffer, screen_width))
    spawn_y = player_y + random.choice([-1, 1]) * (
        random.randint(screen_height // 2 + off_screen_buffer, screen_height))

    crashing_enemy = Enemy(spawn_x, spawn_y, 20, 20, 10, ENEMY_SPEED)
    crashing_enemies.append(crashing_enemy)

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

def handle_bullet_collisions(bullets, target_rect, action):
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet['x'] - 10, bullet['y'] - 10, 20, 20)
        if bullet_rect.colliderect(target_rect):
            action()

def start_game():
    global running
    running = False
    print("Starting Game...")

def open_settings():
    print("Opening settings...")
    # Logic to open settings menu

def quit_game():
    print("Quitting game...")
    pygame.quit()
    sys.exit()

while running:
    cursor_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if pygame.mouse.get_pressed()[0] and current_fireball_cooldown == 0:
        centered_x, centered_y = player_x + player_width // 2, player_y + player_height // 4
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - centered_y, mouse_x - centered_x)
        shoot_base_fireball(centered_x, centered_y, bullets, bullet_speed)
        current_fireball_cooldown = base_fireball_cooldown  # Reset the cooldown

    if current_fireball_cooldown > 0:
        current_fireball_cooldown -= 1

    screen.fill(BLACK)
    draw_tiles(0, 0)
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
        screen.blit(rotated_bullet_image, (
        bullet['x'] - rotated_bullet_image.get_width() / 2, bullet['y'] - rotated_bullet_image.get_height() / 2))

    handle_bullet_collisions(bullets, play_button_rect, start_game)
    handle_bullet_collisions(bullets, settings_button_rect, open_settings)
    handle_bullet_collisions(bullets, quit_button_rect, quit_game)

    screen.blit(frames_down[current_frame], player_pos_on_screen)  # Always render the player looking down

    screen.blit(cursor_image, cursor_pos)
    pygame.display.flip()
    clock.tick(FPS)

# Game loop
show_upgrade_menu = False  # Variable to track if the upgrade menu is shown
while True:
    cursor_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused  # Toggle pause state

            if event.key == pygame.K_g:
                gambling_mode = True
                print("You are now gambling!!")

            if show_upgrade_menu:  # Handle upgrade selection
                if event.key == pygame.K_RETURN and upgrades==0:
                    upgrades=1  # Apply the first fireball upgrade
                    show_upgrade_menu = False
                    paused = False  # Unpause the game after selecting the upgrade
                elif event.key == pygame.K_RETURN and upgrades==1:
                    upgrades=2  # Apply the second fireball upgrade
                    show_upgrade_menu = False
                    paused = False  # Unpause the game after selecting the upgrade
                elif event.key == pygame.K_RETURN and upgrades==2:
                    upgrades=3  # Apply the third fireball upgrade
                    show_upgrade_menu = False
                    paused = False  # Unpause the game after selecting the upgrade
                elif event.key == pygame.K_RETURN and upgrades==3:
                    upgrades=4  # Apply the third fireball upgrade
                    show_upgrade_menu = False
                    paused = False  # Unpause the game after selecting the upgrade
                elif event.key == pygame.K_RETURN and upgrades==4:
                    upgrades=5  # Apply the third fireball upgrade
                    show_upgrade_menu = False
                    paused = False  # Unpause the game after selecting the upgrade
                elif event.key == pygame.K_RETURN and upgrades==5:
                    upgrades=6  # Apply the sixth fireball upgrade
                    show_upgrade_menu = False
                    paused = False  # Unpause the game after selecting the upgrade
                elif event.key == pygame.K_RETURN and upgrades==6:
                    upgrades=7  # Apply the sixth fireball upgrade
                    show_upgrade_menu = False
                    paused = False  # Unpause the game after selecting the upgrade
                elif event.key == pygame.K_RETURN:
                    show_upgrade_menu = False
                    paused = False



    if not paused and not show_upgrade_menu:  # Only update game state if not paused and upgrade menu is not shown
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
        player_hitbox = pygame.Rect(player_x - player_width // 2, player_y - player_height // 2, player_width,player_height)
        center_x = player_x + player_width / 2
        center_y = player_y + player_height / 4
        # Decrease the current fireball cooldown
        if current_fireball_cooldown > 0:
            current_fireball_cooldown -= 1

        # Automatically shoot fireballs if the 7th upgrade is active
        if upgrades==7 and current_fireball_cooldown == 0:
            shoot_base_fireball(player_x, player_y, bullets, bullet_speed)

        # Update frame count and current frame if the player is moving
        if move_x != 0 or move_y != 0:
            frame_count += 1
            if frame_count % 2 == 0:  # Adjust frame rate of animation here
                current_frame = (current_frame + 1) % 3  # Assuming each direction has 3 frames

        if pygame.mouse.get_pressed()[0] and paused is False and not show_upgrade_menu and upgrades!=7 and current_fireball_cooldown==0:
            shoot_base_fireball(player_x, player_y, bullets, bullet_speed)

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
        if kills > 100 and random.randint(0, 10000) == 69:
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

            if (player_x < crashing_enemy.x + crashing_enemy.width and player_x + player_width > crashing_enemy.x and
                    player_y < crashing_enemy.y + crashing_enemy.height and player_y + player_height > crashing_enemy.y):
                if invince_frames == i_frame_temp:
                    player_hp -= 5
                    invince_frames = 0

            # Check for collisions with bullets
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet['x'] - 5, bullet['y'] - 5, 10, 10)
                enemy_rect = pygame.Rect(crashing_enemy.x, crashing_enemy.y, crashing_enemy.width,
                                         crashing_enemy.height)

                if bullet_rect.colliderect(enemy_rect):
                    crashing_enemy.hp -= 10
                    bullets.remove(bullet)

                    if crashing_enemy.hp <= 0:
                        crashing_enemies.remove(crashing_enemy)
                        sys.exit("The corruption is spreading...")

        enemies_to_remove = []
        for enemy in enemies:
            # Calculate the center coordinates of the player
            player_x_center = player_x + player_width / 2
            player_y_center = player_y + player_height / 2

            # Calculate the vertical and horizontal distance between the enemy and the player's center
            distance_y = player_y_center - enemy.y
            distance_x = player_x_center - enemy.x

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
                    if upgrades<=5:
                        bullets.remove(bullet)

                    if enemy.hp <= 0:
                        enemies_to_remove.append(enemy)
                        active_exp_orbs.append({'size': enemy_exp * 5, 'x': enemy.x, 'y': enemy.y, 'value': enemy_exp})
                        enemy_exp = random.randint(1, 5)
                        kills += 1
                        if random.randint(0, 100) == 69:
                            active_regen_orbs.append({'x': enemy.x, 'y': enemy.y, 'size': regen_orb_size, 'value': regen_amount})
                            print("A wild regen orb spawned!!!!!")
                        break

        for enemy in enemies_to_remove:
            enemies.remove(enemy)

        if player_hp <= 0:
            sys.exit("You died...")

        # Check for collisions between player and exp orbs
        for exp_orb in active_exp_orbs:
            orb_center_x = exp_orb['x']
            orb_center_y = exp_orb['y']
            orb_radius = exp_orb['size']
            orb_exp = exp_orb['value']  # Extract the exp value associated with the orb

            # Check for collisions with the player
            if (player_x < orb_center_x + orb_radius and player_x + player_width > orb_center_x - orb_radius and
                    player_y < orb_center_y + orb_radius and player_y + player_height > orb_center_y - orb_radius):
                pickup_sound.play()
                # Player gains exp equal to the amount associated with the exp orb
                exp += orb_exp
                # Remove the exp orb from the active list
                active_exp_orbs.remove(exp_orb)

        for regen_orb in active_regen_orbs:
            orb_center_x = regen_orb['x']
            orb_center_y = regen_orb['y']
            orb_radius = regen_orb['size']
            orb_value = regen_orb['value']  # Extract the exp value associated with the orb

            # Check for collisions with the player
            if (player_x < orb_center_x + orb_radius and player_x + player_width > orb_center_x - orb_radius and
                    player_y < orb_center_y + orb_radius and player_y + player_height > orb_center_y - orb_radius):
                pickup_sound_regen.play()
                # Player gains exp equal to the amount associated with the exp orb
                player_hp += orb_value
                # Remove the exp orb from the active list
                active_regen_orbs.remove(regen_orb)

    # Calculate camera offset
    camera_offset_x = width // 2 - player_x
    camera_offset_y = height // 2 - player_y

    # Draw elements
    screen.fill(BLACK)  # Clear the screen
    draw_tiles(camera_offset_x, camera_offset_y)

    for exp_orb in active_exp_orbs:
        # Resize the exp_image based on the orb's size
        scaled_exp_image = pygame.transform.scale(exp_image, (exp_orb['size'], exp_orb['size']))

        # Calculate the top-left corner of the image so it's centered on the orb's position
        image_x = exp_orb['x'] - scaled_exp_image.get_width() // 2 + camera_offset_x
        image_y = exp_orb['y'] - scaled_exp_image.get_height() // 2 + camera_offset_y

        # Draw the scaled image
        screen.blit(scaled_exp_image, (image_x, image_y))

    for regen_orb in active_regen_orbs:
        # Resize the exp_image based on the orb's size
        scaled_regen_image = pygame.transform.scale(regen_image, (regen_orb_size * 2, regen_orb_size * 2))

        # Calculate the top-left corner of the image so it's centered on the orb's position
        image_x = regen_orb['x'] - scaled_regen_image.get_width() // 2 + camera_offset_x
        image_y = regen_orb['y'] - scaled_regen_image.get_height() // 2 + camera_offset_y

        # Draw the scaled image
        screen.blit(scaled_regen_image, (image_x, image_y))

    for enemy in enemies:
        # Animate and draw enemy
        enemy.frame_count += 1
        if enemy.frame_count % 10 == 0 and not paused:  # Adjust frame rate of animation here
            enemy.frame = (enemy.frame + 1) % len(enemy_frames)

        # Draw enemy using current frame
        enemy_image = enemy_frames[enemy.frame]
        screen.blit(enemy_image, (enemy.x + camera_offset_x, enemy.y + camera_offset_y))

    for crashing_enemy in crashing_enemies and not paused:
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
    draw_coordinates(player_x, player_y)
    if rendering == "right":
        screen.blit(frames_right[current_frame], (player_pos_on_screen))  # Draw the current frame of player sprite
    if rendering == "up":
        screen.blit(frames_up[current_frame], (player_pos_on_screen))
    if rendering == "left":
        screen.blit(frames_left[current_frame], (player_pos_on_screen))
    if rendering == "down":
        screen.blit(frames_down[current_frame], (player_pos_on_screen))
    if invince_frames < i_frame_temp:
        invince_frames += 1
    if exp >= current_max_exp:
        level_up()

    # If game is paused, show pause menu
    if paused and not show_upgrade_menu:
        pause_text = menu_font.render("PAUSED", True, WHITE)
        text_width, text_heights = menu_font.size("PAUSED")
        text_x = (width - text_width) // 2
        text_y = (height - text_heights) // 2
        screen.blit(pause_text, (text_x, text_y))

    # If upgrade menu is shown, display upgrade options
    if show_upgrade_menu:
        if upgrades == 0:
            upgrade_text1 = menu_font.render("1. Fireball shoots in opposite direction", True, WHITE)
            text_width, text_height = menu_font.size("1. Fireball shoots in opposite direction")
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 + 50
            screen.blit(upgrade_text1, (text_x, text_y))
        elif upgrades == 1:
            upgrade_text2 = menu_font.render("2. Fireball shoots in the right direction", True, WHITE)
            text_width, text_height = menu_font.size("2. Fireball shoots in the right direction")
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 + 50
            screen.blit(upgrade_text2, (text_x, text_y))
        elif upgrades == 2:
            upgrade_text3 = menu_font.render("3. Fireball shoots in the left direction", True, WHITE)
            text_width, text_height = menu_font.size("3. Fireball shoots in the left direction")
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 + 50
            screen.blit(upgrade_text3, (text_x, text_y))
        elif upgrades == 3:
            upgrade_text4 = menu_font.render("4. Fireball shoots in the top left and right direction", True, WHITE)
            text_width, text_height = menu_font.size("4. Fireball shoots in the top left and right direction")
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 + 50
            screen.blit(upgrade_text4, (text_x, text_y))
        elif upgrades == 4:
            upgrade_text5 = menu_font.render("5. Fireball shoots in the bottom left and right direction", True, WHITE)
            text_width, text_height = menu_font.size("5. Fireball shoots in the bottom left and right direction")
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 + 50
            screen.blit(upgrade_text5, (text_x, text_y))
        elif upgrades == 5:
            upgrade_text6 = menu_font.render("6. Fireball goes through enemies", True, WHITE)
            text_width, text_height = menu_font.size("6. Fireball goes through enemies")
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 + 50
            screen.blit(upgrade_text6, (text_x, text_y))
        elif upgrades == 6:
            upgrade_text7 = menu_font.render("7. Automode", True, WHITE)
            text_width, text_height = menu_font.size("7. Automode")
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 + 50
            screen.blit(upgrade_text7, (text_x, text_y))
        elif upgrades >= 7:
            out_of_upgrades_text = menu_font.render("So um funny story, I'm out of upgrade ideas...", True, WHITE)
            text_width, text_height = menu_font.size("So um funny story, I'm out of upgrade ideas...")
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 + 50
            screen.blit(out_of_upgrades_text, (text_x, text_y))
    screen.blit(cursor_image, cursor_pos)

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)
