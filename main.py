import math
import pygame
import sys
import random
from base_enemy import Enemy, enemies
from crashing_enemy import crashingEnemy, crashing_enemies
from bulky_enemy import Bulky, bulkies
from corrupted_enemy import Corrupty, corrupties
import os

# Initialize pygame
pygame.init()
# Initialize pygame.mixer
pygame.mixer.init()
# Make default cursor invisible
pygame.mouse.set_visible(False)

fullscreen = False # Set Fullscreen to false by default
volume = 0.5  # Set default volume

if fullscreen:
    # Set up the display in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = pygame.display.get_surface().get_size() # Get screen dimensions
else:
    # Set up the display in windowed mode
    screen_width = 690  # Width of the window
    screen_height = 690  # Height of the window
    screen = pygame.display.set_mode((screen_width, screen_height))  # Setup window

width, height = pygame.display.get_surface().get_size()  # Obtain dimensions of the game window
pygame.display.set_caption("Bullet Heaven")  # Set the title of the window
FPS = 60  # Set FPS
clock = pygame.time.Clock()  # Used to control frame rate
main_menu = True  # Enables main menu

# Load and scale images
tile_image = pygame.image.load('sprites/tile.png')
corrupted_tile_image = pygame.image.load('sprites/corrupted_tile.png')
tile_x = 1011
tile_y = 624
scaled_tile_image = pygame.transform.scale(tile_image, (tile_x, tile_y))
scaled_corrupted_tile_image = pygame.transform.scale(corrupted_tile_image, (tile_x, tile_y))
cursor_image = pygame.image.load("sprites/cursor.png")
title_image = pygame.image.load("sprites/title.png")
play_button_image = pygame.image.load('sprites/play.png')
settings_button_image = pygame.image.load('sprites/settings.png')
quit_button_image = pygame.image.load('sprites/quit.png')
title_scaled_width = title_image.get_width() / 2
title_scaled_height = title_image.get_height() / 2
scaled_title_image = pygame.transform.scale(title_image, (title_scaled_width, title_scaled_height))
exp_image = pygame.image.load("sprites/exp.png")
regen_image = pygame.image.load("sprites/regen_orb.png")

# Positions of play, settings and quit button
title_rect = scaled_title_image.get_rect(center=(width / 2, height / 4))
play_button_rect = play_button_image.get_rect(center=(width / 4, height / 2))
settings_button_rect = settings_button_image.get_rect(center=(width / 2, height - height / 5))
quit_button_rect = quit_button_image.get_rect(center=(3 * width / 4, height / 2))




# Load sprite sheet for the character walking. Convert alpha is used for performance optimization
sprite_sheet_right = pygame.image.load('sprites/Niko_right.png').convert_alpha()
sprite_sheet_up = pygame.image.load('sprites/Niko_up.png').convert_alpha()
sprite_sheet_down = pygame.image.load('sprites/Niko_down.png').convert_alpha()
sprite_sheet_left = pygame.image.load('sprites/Niko_left.png').convert_alpha()

# Sprite setup
frame_width, frame_height = 24, 30  # Width and height of each sprite frame
scaling_factor = 2.77  # Scaling factor for sprite
niko_scaling_width, niko_scaling_height = frame_width * scaling_factor, frame_height * scaling_factor  # Scaled dimensions of sprite

# Animate sprites
# Subsurface extracts the defined rectangle from the sprite sheet
# Then it gets scaled to the defined height and width
frames_up = [pygame.transform.scale(sprite_sheet_up.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (niko_scaling_width, niko_scaling_height)) for i in range(3)]
frames_right = [pygame.transform.scale(sprite_sheet_right.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (niko_scaling_width, niko_scaling_height)) for i in range(3)]
frames_down = [pygame.transform.scale(sprite_sheet_down.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (niko_scaling_width, niko_scaling_height)) for i in range(3)]
frames_left = [pygame.transform.scale(sprite_sheet_left.subsurface(pygame.Rect(frame_width * i, 0, frame_width, frame_height)), (niko_scaling_width, niko_scaling_height)) for i in range(3)]
rendering = "down"  # Make sure the sprite spawns facing down

# Used to track frames
current_frame = 0  # Current frame index for animation
frame_count = 0  # Frame counter for animation timing



# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Player attributes
player_x = width // 2  # Initial player x position
player_y = height // 2  # Initial player y position
player_pos_on_screen = width//2-25, height//2  # Player position on screen
player_speed = 5  # Player movement speed
player_height = int(niko_scaling_height)  # Player height
player_width = int(niko_scaling_width)  # Player width
player_hp = 100  # Player health points
i_frames_counter = 0  # Invincibility frames counter
i_frames = 10  # Number of invincibility frames
kills = 0  # Kill count

# Experience system
exp = 0  # Player experience points
enemy_exp = random.randint(1, 5)  # Amount of Experience points dropped by enemies
active_exp_orbs = []  # List of active experience orbs
current_max_exp = 30  # Experience required for next level
player_level = 1  # Current player level (by default)
exp_increase_per_level = 5  # Experience increase per level

# Load some more sounds
pickup_sound = pygame.mixer.Sound("sounds/exp.wav")
pickup_sound_regen = pygame.mixer.Sound("sounds/pickup_regen.wav")
level_up_sound = pygame.mixer.Sound("sounds/level_up_normal.wav")
gambling_sound = pygame.mixer.Sound("sounds/gambling.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
explooosion_sound = pygame.mixer.Sound("sounds/explooosion.wav")

# Regeneration
active_regen_orbs = []  # List of active regeneration orbs
regen_amount = 30  # Amount of health regenerated by orbs
regen_orb_size = 15  # Size of regeneration orbs

# Bullet attributes
bullets = []  # List of active bullets
bullet_speed = 10  # Bullet speed
bullet_frames = []  # List of bullet frames for animation
BULLET_DAMAGE = 10.5  # Default amount of damage the bullet does

for i in range(1, 6):  # There are five fireball images named fireball1.png through fireball5.png
    bullet_original_frame = pygame.image.load(f"sprites/fireball{i}.png").convert_alpha()  # Load bullet frame
    bullet_scaled_width = bullet_original_frame.get_width() * 2   # Scale bullet width
    bullet_scaled_height = bullet_original_frame.get_height() * 2  # Scale bullet height
    bullet_scaled_frame = pygame.transform.scale(bullet_original_frame, (bullet_scaled_width, bullet_scaled_height))  # Scale bullet frame
    bullet_frames.append(bullet_scaled_frame)  # Add scaled bullet frame to list

ENEMY_SPEED = 0.75  # Base enemy speed
ENEMY_HP = 10  # Base enemy health points
SPEED_SCALING_FACTOR = 0.005  # Increase in speed per kill
HP_SCALING_FACTOR = 0.01     # Increase in HP per kill

# Some flags for checking things
gambling_mode = False  # Gambling mode flag (false by default)
bulky_spawned = False
corrupty_spawned = False
corruption = False
settings_open = False
right_mouse_button_pressed = False
paused = False
explosion = False

# Load base enemy frames
enemy_frames = []
for i in range(1, 5):  # There are 4 enemy images named bat1.png to bat4.png
    enemy_original_frame = pygame.image.load(f"sprites/enemies/bat{i}.png").convert_alpha()  # Load enemy frame
    enemy_scaled_width = enemy_original_frame.get_width() * 2.5  # Scale enemy width
    enemy_scaled_height = enemy_original_frame.get_height() * 2.5  # Scale enemy height
    enemy_scaled_frame = pygame.transform.scale(enemy_original_frame, (enemy_scaled_width, enemy_scaled_height))  # Scale enemy frame
    enemy_frames.append(enemy_scaled_frame)  # Add scaled enemy frame to list

# Load base enemy hit frames
hit_enemy_frames = []
for i in range(1, 6):  # There are 5 enemy hit images named bathit1.png to bathit5.png
    hit_enemy_original_frame = pygame.image.load(f"sprites/enemies/bathit{i}.png").convert_alpha()  # Load enemy hit frame
    hit_enemy_scaled_width = hit_enemy_original_frame.get_width() * 2.5  # Scale enemy hit frame width
    hit_enemy_scaled_height = hit_enemy_original_frame.get_height() * 2.5  # Scale enemy hit frame height
    hit_enemy_scaled_frame = pygame.transform.scale(hit_enemy_original_frame, (hit_enemy_scaled_width, hit_enemy_scaled_height))  # Scale enemy hit frame
    hit_enemy_frames.append(hit_enemy_scaled_frame)  # Add scaled enemy hit frame to list

# Load base enemy death frames
death_enemy_frames = []
for i in range(1, 6):  # Assuming there are 5 enemy death images named batdeath1.png to batdeath5.png
    death_enemy_original_frame = pygame.image.load(f"sprites/enemies/batdeath{i}.png").convert_alpha()  # Load enemy death frame
    death_enemy_scaled_width = death_enemy_original_frame.get_width() * 2.5  # Scale enemy death frame width
    death_enemy_scaled_height = death_enemy_original_frame.get_height() * 2.5  # Scale enemy death frame height
    death_enemy_scaled_frame = pygame.transform.scale(death_enemy_original_frame, (death_enemy_scaled_width, death_enemy_scaled_height))  # Scale enemy death frame
    death_enemy_frames.append(death_enemy_scaled_frame)  # Add scaled enemy death frame to list

# Load bulky enemy frames
bulky_frames = []
for i in range(1, 17):  # There are 17 bulky images named slime1.png to slime17.png
    bulky_original_frame = pygame.image.load(f"sprites/enemies/slime{i}.png").convert_alpha()  # Load bulky frame
    bulky_scaled_width = bulky_original_frame.get_width() * 5  # Scale bulky width
    bulky_scaled_height = bulky_original_frame.get_height() * 5  # Scale bulky height
    bulky_scaled_frame = pygame.transform.scale(bulky_original_frame, (bulky_scaled_width, bulky_scaled_height))  # Scale bulky frame
    bulky_frames.append(bulky_scaled_frame)  # Add scaled bulky frame to list

bulky_death_frames = []
for i in range(1, 7):  # There are 6 bulky death images named slimedeath1.png to slimedeath6.png
    bulky_death_original_frame = pygame.image.load(f"sprites/enemies/slimedeath{i}.png").convert_alpha()  # Load bulky death frame
    bulky_death_scaled_width = bulky_death_original_frame.get_width() * 3  # Scale bulky death frame width
    bulky_death_scaled_height = bulky_death_original_frame.get_height() * 3  # Scale bulky death frame height
    bulky_death_scaled_frame = pygame.transform.scale(bulky_death_original_frame, (bulky_death_scaled_width, bulky_death_scaled_height))  # Scale bulky death frame
    bulky_death_frames.append(bulky_death_scaled_frame) # Add scaled bulky death frame to list

corrupty_frames = []
for i in range(1, 5):  # There are 4 corrupty images named glitch1.png to glitch4.png
    corrupty_original_frame = pygame.image.load(f"sprites/enemies/glitch{i}.png").convert_alpha()  # Load corrupty frame
    corrupty_scaled_width = corrupty_original_frame.get_width() / 7  # Scale corrupty width
    corrupty_scaled_height = corrupty_original_frame.get_height() / 7  # Scale corrupty height
    corrupty_scaled_frame = pygame.transform.scale(corrupty_original_frame, (corrupty_scaled_width, corrupty_scaled_height))  # Scale corrupty frame
    corrupty_frames.append(corrupty_scaled_frame)  # Add scaled corrupty frame to list

crashing_enemy_frames = []
for i in range(1, 9):  # There are 8 crashing enemy images named skull1.png to skull8.png
    crashing_enemy_original_frame = pygame.image.load(f"sprites/enemies/skull{i}.png").convert_alpha()  # Load crashing enemy frame
    crashing_enemy_scaled_width = crashing_enemy_original_frame.get_width() * 3  # Scale crashing enemy width
    crashing_enemy_scaled_height = crashing_enemy_original_frame.get_height() * 3  # Scale crashing enemy height
    crashing_enemy_scaled_frame = pygame.transform.scale(crashing_enemy_original_frame, (crashing_enemy_scaled_width, crashing_enemy_scaled_height))  # Scale crashing enemy frame
    crashing_enemy_frames.append(crashing_enemy_scaled_frame)  # Add scaled crashing enemy frame to list


# Load fireball sounds
fireball_sound_1 = pygame.mixer.Sound("sounds/fireball1.wav")
fireball_sound_2 = pygame.mixer.Sound("sounds/fireball2.wav")
fireball_sound_3 = pygame.mixer.Sound("sounds/fireball3.wav")
fireball_sound_4 = pygame.mixer.Sound("sounds/fireball4.wav")
fireball_sound_5 = pygame.mixer.Sound("sounds/fireball5.wav")
fireball_sound_6 = pygame.mixer.Sound("sounds/fireball6.wav")
fireball_sound_7 = pygame.mixer.Sound("sounds/fireball7.wav")

base_fireball_cooldown = 50  # Base cooldown for fireball
current_fireball_cooldown = 0  # Current cooldown for fireball
upgrades = 0  # Number of upgrades (by default)

cooldown_reduction_upgrade1 = 10  # Cooldown reduction Upgrade 1
cooldown_reduction_upgrade2 = 5  # Cooldown reduction Upgrade 2
cooldown_reduction_upgrade3 = 10  # Cooldown reduction Upgrade 3
cooldown_reduction_upgrade4 = 5  # etc etc
cooldown_reduction_upgrade5 = 5
cooldown_reduction_upgrade6 = -40
cooldown_reduction_upgrade7 = 10

# Settings
volume = 0.5
# Brightness and contrast don't actually have a function currently
brightness = 0.5
contrast = 0.5

# Fonts
menu_font = pygame.font.SysFont('Avenir', 30)

documents_path = os.path.expanduser("~/")  # Define the file path to home directory
file_path = os.path.join(documents_path, "savefile.bulletheaven")  # Path to save file

# Check if the file exists
if os.path.exists(file_path):
    # Read data from the file and assign to variables
    with open(file_path, "r") as file:
        lines = file.readlines()
        upgrades = int(lines[0].strip())
        kills = int(lines[1].strip())
        player_hp = int(lines[2].strip())
        exp = int(lines[3].strip())
        player_level = int(lines[4].strip())
        corruption = lines[5].strip() == "True"
        current_max_exp = int(lines[6].strip())

# Set background music based on corruption state. These are unaffected by volume
if not corruption:
    music = pygame.mixer.Sound('sounds/background_music.mp3')
else:
    music = pygame.mixer.Sound('sounds/corrupted.mp3')

def save():
    # Write the current game state to the file
    with open(file_path, "w") as file:
        file.write(f"{upgrades}\n")
        file.write(f"{kills}\n")
        file.write(f"{player_hp}\n")
        file.write(f"{exp}\n")
        file.write(f"{player_level}\n")
        file.write(f"{corruption}\n")
        file.write(f"{current_max_exp}\n")


def draw_tiles(camera_offset_x, camera_offset_y):
    # Draw background tiles, choosing corrupted or normal based on corruption state
    tile_to_draw = scaled_corrupted_tile_image if corruption != 0 else scaled_tile_image
    for y in range(-tile_y, height + tile_y, tile_y):
        for x in range(-tile_x, width + tile_x, tile_x):
            screen.blit(tile_to_draw, (x + camera_offset_x % tile_x - tile_x, y + camera_offset_y % tile_y - tile_y))

def animate_bullet(bullet):
    # Update bullet frame for animation
    bullet['frame'] += 1
    if bullet['frame'] >= len(bullet_frames):  # Loop back to the first frame if at the end
        bullet['frame'] = 0
    return bullet_frames[bullet['frame']]  # Return the current frame of the bullet

def shoot_forwards(player_x, player_y,bullet_speed,angle, bullets):
    # Shoot a bullet forwards from the player
    bullets.append({
        'x': player_x,  # Starting x position
        'y': player_y,  # Starting y position
        'dx': bullet_speed * math.cos(angle),  # Change in x based on speed and angle
        'dy': bullet_speed * math.sin(angle),  # Change in y based on speed and angle
        'frame': 0  # Start with the first frame of the bullet animation
    })
def shoot_backwards(player_x, player_y,bullet_speed, angle, bullets):
    # Shoot a bullet backwards from the player
    backwards_angle = angle + math.pi  # Calculate opposite angle
    bullets.append({
        'x': player_x,  # Same here etc
        'y': player_y,
        'dx': bullet_speed * math.cos(backwards_angle),
        'dy': bullet_speed * math.sin(backwards_angle),
        'frame': 0
    })

def shoot_right(player_x, player_y,bullet_speed, angle, bullets):
    # Shoot a bullet to the right of the player
    right_angle = angle + math.pi / 2  # Angle for right direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(right_angle),
        'dy': bullet_speed * math.sin(right_angle),
        'frame': 0
    })

def shoot_left(player_x, player_y,bullet_speed, angle, bullets):
    # Shoot a bullet to the left of the player
    left_angle = angle - math.pi / 2  # Angle for left direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(left_angle),
        'dy': bullet_speed * math.sin(left_angle),
        'frame': 0
    })

def shoot_up_directional(player_x, player_y,bullet_speed, angle, bullets):
    # Shoot a bullet to the forward right direction of the player
    upright_angle = angle + math.pi / 4  # Angle for upright direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(upright_angle),
        'dy': bullet_speed * math.sin(upright_angle),
        'frame': 0
    })
    # Shoot a bullet to the forward left direction of the player
    upleft_angle = angle - math.pi / 4  # Angle for upleft direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(upleft_angle),
        'dy': bullet_speed * math.sin(upleft_angle),
        'frame': 0
    })

def shoot_down_directional(player_x, player_y,bullet_speed, angle, bullets):
    # Shoot a bullet to the backwards right direction of the player
    downright_angle = angle + 3 * math.pi / 4  # Angle for upright direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(downright_angle),
        'dy': bullet_speed * math.sin(downright_angle),
        'frame': 0
    })
    # Shoot a bullet to the backwards left direction of the player
    downleft_angle = angle - 3 * math.pi / 4  # Angle for upleft direction
    bullets.append({
        'x': player_x,
        'y': player_y,
        'dx': bullet_speed * math.cos(downleft_angle),
        'dy': bullet_speed * math.sin(downleft_angle),
        'frame': 0
    })

def shoot_base_fireball(player_x, player_y, bullets, bullet_speed):
    global current_fireball_cooldown
    centered_x, centered_y = player_x+player_width//2-25, player_y+player_height//4  # Center of player
    mouseX, mouseY = pygame.mouse.get_pos()  # Get mouse position
    angle = math.atan2(mouseY-height//2-player_height//4, mouseX-width//2-player_width//2+25)  # Use the center of the screen for calculating the angle of the fireball
    if upgrades >= 7:  # If the 7th upgrade is active, shoot in all directions and automatically shoot upwards
        fireball_sound_7.play()  # Play fireball sound 7
        up = -math.pi / 2  # Angle for shooting upwards
        shoot_forwards(centered_x, centered_y, bullet_speed, up, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, up, bullets)
        shoot_right(centered_x, centered_y, bullet_speed, up, bullets)
        shoot_left(centered_x, centered_y, bullet_speed, up, bullets)
        shoot_up_directional(centered_x, centered_y, bullet_speed, up, bullets)
        shoot_down_directional(centered_x, centered_y, bullet_speed, up, bullets)

    if upgrades == 0:  # If no upgrade is active, shoot forwards
        fireball_sound_1.play()  # Play fireball sound 1
        shoot_forwards(centered_x, centered_y, bullet_speed,angle, bullets)
    elif upgrades == 1:  # If 1st upgrade is active, shoot forwards and backwards
        fireball_sound_2.play() # Same thing here...
        shoot_forwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, angle, bullets)
    elif upgrades == 2:  # If 2nd upgrade is active, shoot forwards, backwards and right
        fireball_sound_3.play()
        shoot_forwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_right(centered_x, centered_y, bullet_speed, angle, bullets)
    elif upgrades == 3:  # If 3rd upgrade is active, shoot forwards, backwards, right and left
        fireball_sound_4.play()
        shoot_forwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_right(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_left(centered_x, centered_y, bullet_speed, angle, bullets)
    elif upgrades == 4:  # Etc, you get the idea
        fireball_sound_5.play()
        shoot_forwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_backwards(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_right(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_left(centered_x, centered_y, bullet_speed, angle, bullets)
        shoot_up_directional(centered_x, centered_y, bullet_speed, angle, bullets)
    elif upgrades == 5 or upgrades == 6:
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
        cooldown_reduction += cooldown_reduction_upgrade1  # Add cooldown reduction for upgrade 1
    if upgrades == 2:
        cooldown_reduction += cooldown_reduction_upgrade2  # Add cooldown reduction for upgrade 2
    if upgrades == 3:
        cooldown_reduction += cooldown_reduction_upgrade3  # etc, you get the idea
    if upgrades == 4:
        cooldown_reduction += cooldown_reduction_upgrade4
    if upgrades == 5:
        cooldown_reduction += cooldown_reduction_upgrade5
    if upgrades == 6:
        cooldown_reduction += cooldown_reduction_upgrade6
    if upgrades == 7:
        cooldown_reduction += cooldown_reduction_upgrade7
    current_fireball_cooldown = base_fireball_cooldown - cooldown_reduction  # Apply the reduced cooldown

def draw_kill_counter(kills):
    # Draw the kill counter on the screen
    font = pygame.font.SysFont('Avenir', 15)  # Define font
    kills_text = font.render(f"Kills: {kills}", True, RED)  # Render kill text
    text_width, text_height = font.size(f"Kills: {kills}")  # Get text dimensions
    text_x = (width - text_width) / 20  # Calculate x position
    text_y = 40  # Set y position
    screen.blit(kills_text, (text_x, text_y))  # Draw kill counter

def draw_explosion_cooldown(explosion_cooldown):
    # Draw the explosion cooldown on the screen
    font = pygame.font.SysFont('Avenir', 15)  # Define font
    text = font.render(f"Explosion Cooldown: {explosion_cooldown}", True, WHITE)  # Render cooldown text
    text_width, text_height = font.size(f"Explosion Cooldown: {explosion_cooldown}")  # Get text dimensions
    text_x = (width - text_width)  # Calculate x position
    text_y = height - 30  # Set y position
    screen.blit(text, (text_x, text_y))  # Draw explosion cooldown

def draw_coordinates(player_x, player_y):
    # Draw the player's coordinates on the screen
    font = pygame.font.SysFont('Avenir', 15)  # Define font
    coordinate_text = font.render(f"Coordinates: {int(player_x)}:{int(player_y)}", True, WHITE)  # Render coordinates text
    text_width, text_height = font.size(f"Coordinates: {coordinate_text}")  # Get text dimensions
    text_x = (width - text_width) / 20 * 24  # Calculate x position
    text_y = 40  # Set y position
    screen.blit(coordinate_text, (text_x, text_y))  # Draw coordinates

# level up function
def level_up():
    global player_level, exp, current_max_exp, paused, show_upgrade_menu  # Declare global variables
    player_level += 1 # Increase player level
    exp -= current_max_exp  # Subtract current max exp from player's exp
    current_max_exp = int(current_max_exp * 1.3)  # Increase current max exp exponentially for the next level
    paused = True  # Pause the game
    show_upgrade_menu = True  # Show the upgrade menu
    if gambling_mode:
        gambling_sound.play()  # Play gambling sound if gambling mode is active
    else:
        level_up_sound.play()  # Play level up sound if not in gambling mode

# Function to draw experience bar
def draw_exp_bar():
    max_exp = current_max_exp  # Maximum experience for current level
    exp_bar_width = width - 20  # Define the width of the experience bar
    exp_bar_height = 20  # Define the height of the experience bar
    exp_indicator_width = int(exp / max_exp * exp_bar_width)  # Calculate the width of the experience indicator

    pygame.draw.rect(screen, BLUE, (10, 10, exp_bar_width, exp_bar_height))  # Blue background
    pygame.draw.rect(screen, GREEN, (10, 10, exp_indicator_width, exp_bar_height))  # Green indicator

    font = pygame.font.SysFont('Avenir', 15)  # Define font
    exp_text = font.render(f"EXP: {exp}/{max_exp}", True, WHITE)  # Render exp text
    text_width, text_height = font.size(f"EXP: {exp}/{max_exp}")  # Get text dimensions
    text_x = (width - text_width) / 2  # Calculate x position
    text_y = exp_bar_height + 20   # Set y position
    screen.blit(exp_text, (text_x, text_y))  # Draw exp text

# Function to spawn enemies
def spawn_enemy(player_x, player_y):
    global scaled_speed, scaled_hp
    # Calculate the boundaries for off-screen spawning
    off_screen_buffer = 10  # Distance outside the screen to ensure spawning off-screen
    spawn_x = player_x + random.choice([-1, 1]) * (random.randint(screen_width // 2 + off_screen_buffer, screen_width))
    spawn_y = player_y + random.choice([-1, 1]) * (random.randint(screen_height // 2 + off_screen_buffer, screen_height))

    scaled_speed = ENEMY_SPEED + kills * SPEED_SCALING_FACTOR
    scaled_hp = ENEMY_HP + kills * HP_SCALING_FACTOR

    basic_enemy = Enemy(spawn_x, spawn_y, enemy_scaled_width, enemy_scaled_height, scaled_hp, scaled_speed)
    enemies.append(basic_enemy)

# Function to spawn crashing enemies
def spawn_crashing_enemy(player_x, player_y):
    off_screen_buffer = 10  # Distance outside the screen to ensure spawning off-screen
    spawn_x = player_x + random.choice([-1, 1]) * (random.randint(screen_width // 2 + off_screen_buffer, screen_width))
    spawn_y = player_y + random.choice([-1, 1]) * (random.randint(screen_height // 2 + off_screen_buffer, screen_height))

    crashing_enemy = crashingEnemy(spawn_x, spawn_y, crashing_enemy_scaled_width, crashing_enemy_scaled_height, 10, ENEMY_SPEED)
    crashing_enemies.append(crashing_enemy)

def spawn_bulky(player_x, player_y):
    global bulky_spawned
    off_screen_buffer = 10  # Distance outside the screen to ensure spawning off-screen
    spawn_x = player_x + random.choice([-1, 1]) * (random.randint(screen_width // 2 + off_screen_buffer, screen_width))
    spawn_y = player_y + random.choice([-1, 1]) * (random.randint(screen_height // 2 + off_screen_buffer, screen_height))
    print("Spawned a Slime at", spawn_x, spawn_y)
    bulky = Bulky(spawn_x, spawn_y, bulky_scaled_width, bulky_scaled_height, 100, 0.7)
    bulkies.append(bulky)
    bulky_spawned = True

def spawn_corrupty(player_x, player_y):
    global corrupty_spawned, ENEMY_SPEED
    off_screen_buffer = 10  # Distance outside the screen to ensure spawning off-screen
    spawn_x = player_x + random.choice([-1, 1]) * (random.randint(screen_width // 2 + off_screen_buffer, screen_width))
    spawn_y = player_y + random.choice([-1, 1]) * (random.randint(screen_height // 2 + off_screen_buffer, screen_height))
    print("Something happened at", spawn_x, spawn_y, "...")
    corrupty = Corrupty(spawn_x, spawn_y, corrupty_scaled_width, corrupty_scaled_height, 200, ENEMY_SPEED*1.75)  # Example values for width, height, hp, and speed
    corrupties.append(corrupty)
    corrupty_spawned = True

# Function to draw player's health bar
def draw_hp_bar():
    hp_bar_width = player_hp * 2
    hp_bar_height = 20
    hp_indicator_width = int(player_hp / 100 * hp_bar_width)

    pygame.draw.rect(screen, RED, (10, height - 30, hp_bar_width, hp_bar_height))  # Red background
    pygame.draw.rect(screen, GREEN, (10, height - 30, hp_indicator_width, hp_bar_height))  # Green indicator
    font =pygame.font.SysFont('Avenir', 20, False)
    hp_text = font.render(f"{player_hp}/100 HP", True, RED)
    screen.blit(hp_text, (220, height - 30))

def handle_bullet_collisions(bullets, target_rect, action):
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet['x'] - 10, bullet['y'] - 10, 20, 20)
        if bullet_rect.colliderect(target_rect):
            action()

def start_game():
    global main_menu
    main_menu = False
    print("Starting Game...")


def open_main_settings():
    global volume, brightness, contrast
    bullets.remove(bullet)
    settings = [
        {"name": "Volume", "value": volume, "min": 0.0, "max": 1.0, "step": 0.1},
        {"name": "Brightness", "value": brightness, "min": 0.0, "max": 1.0, "step": 0.1},
        {"name": "Contrast", "value": contrast, "min": 0.0, "max": 1.0, "step": 0.1},
    ]

    selected_index = 0
    settings_open = True
    while settings_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings_open = False
                if event.key == pygame.K_w:
                    selected_index = (selected_index - 1) % len(settings)
                if event.key == pygame.K_s:
                    selected_index = (selected_index + 1) % len(settings)
                if event.key == pygame.K_d:
                    settings[selected_index]["value"] = min(settings[selected_index]["value"] + settings[selected_index]["step"], settings[selected_index]["max"])
                if event.key == pygame.K_a:
                    settings[selected_index]["value"] = max(settings[selected_index]["value"] - settings[selected_index]["step"], settings[selected_index]["min"])

        # Update settings values
        volume = settings[0]["value"]
        brightness = settings[1]["value"]
        contrast = settings[2]["value"]

        # Update volume for all sounds
        pickup_sound.set_volume(volume)
        level_up_sound.set_volume(volume)
        gambling_sound.set_volume(volume)
        pickup_sound_regen.set_volume(volume)
        fireball_sound_1.set_volume(volume)
        fireball_sound_2.set_volume(volume)
        fireball_sound_3.set_volume(volume)
        fireball_sound_4.set_volume(volume)
        fireball_sound_5.set_volume(volume)
        fireball_sound_6.set_volume(volume)
        fireball_sound_7.set_volume(volume)
        explosion_sound.set_volume(volume)
        explooosion_sound.set_volume(volume)

        screen.fill(BLACK)
        draw_tiles(0, 0)

        for i, setting in enumerate(settings):
            color = YELLOW if i == selected_index else WHITE
            setting_text = menu_font.render(f"{setting['name']}: {int(setting['value'] * 100)}%", True, color)
            screen.blit(setting_text, (width // 2 - setting_text.get_width() // 2, height // 2 - 50 + i * 40))

        pygame.display.flip()
        clock.tick(FPS)

# spawn explosion
# Function to spawn explosion at given coordinates
def spawn_explosion(x, y, camera_offset_x, camera_offset_y):
    global explosion, explosion_x, explosion_y, explosion_frame_index, explosion_frame_duration, right_mouse_button_pressed, explosion_cooldown
    if gambling_mode:
        explooosion_sound.play()
    else:
        explosion_sound.play()
    right_mouse_button_pressed = False
    explosion = True
    explosion_x = x - camera_offset_x
    explosion_y = y - camera_offset_y
    explosion_frame_index = 0
    explosion_frame_duration = 4  # Adjust as needed for animation speed
    explosion_cooldown = 1000

# Load explosion frames
explosion_frames = []
for i in range(1, 9):
    filename = f'sprites/explosion{i}.png'
    explosion_image = pygame.image.load(filename).convert_alpha()
    explosion_image = pygame.transform.scale(explosion_image, (100, 100))  # Scale to 100x100 pixels
    explosion_frames.append(explosion_image)

# Initialize explosion variables
explosion = False
explosion_x = 0
explosion_y = 0
explosion_frame_index = 0
explosion_frame_duration = 4
explosion_cooldown = 1000
EXPLOSION_DAMAGE = 1.25
explosion_radius = 50  # Adjust this based on the size of your explosion

# Check for collisions with the explosion
def check_explosion_collisions(explosion_x, explosion_y):
    global enemy_exp, corruption, kills
    explosion_rect = pygame.Rect(explosion_x - explosion_radius, explosion_y - explosion_radius,
                                 explosion_radius * 2, explosion_radius * 2)

    # Check collision with enemies
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
        if explosion_rect.colliderect(enemy_rect):
            enemy.hp -= EXPLOSION_DAMAGE
            if enemy.hp <= 0:
                enemies.remove(enemy)
                kills += 1
                active_exp_orbs.append(
                    {'size': enemy_exp * 5, 'x': enemy.x, 'y': enemy.y, 'value': enemy_exp})
                enemy_exp = random.randint(1, 5)


    # Check collision with bulkies
    for bulky in bulkies:
        bulky_rect = pygame.Rect(bulky.x, bulky.y, bulky.width, bulky.height)
        if explosion_rect.colliderect(bulky_rect):
            bulky.hp -= EXPLOSION_DAMAGE
            if bulky.hp <= 0:
                kills += 1
                bulky.death_animation_playing = True
                bulkies.remove(bulky)

    # Check collision with corrupties
    for corrupty in corrupties:
        corrupty_rect = pygame.Rect(corrupty.x, corrupty.y, corrupty.width, corrupty.height)
        if explosion_rect.colliderect(corrupty_rect):
            corrupty.hp -= EXPLOSION_DAMAGE
            if corrupty.hp <= 0:
                corrupties.remove(corrupty)
                kills += 1
                active_exp_orbs.append({'size': enemy_exp * 5, 'x': corrupty.x, 'y': corrupty.y, 'value': enemy_exp})
                enemy_exp = random.randint(1, 5)
                print("You've freed us all!")
                show_victory_screen()

    # Check collision with crashing_enemies
    for crashing_enemy in crashing_enemies:
        crashing_enemy_rect = pygame.Rect(crashing_enemy.x, crashing_enemy.y, crashing_enemy.width, crashing_enemy.height)
        if explosion_rect.colliderect(crashing_enemy_rect):
            crashing_enemy.hp -= EXPLOSION_DAMAGE
            if crashing_enemy.hp <= 0:
                kills += 1
                crashing_enemies.remove(crashing_enemy)
                corruption = True
                kills = 0
                save()
                sys.exit("The corruption is spreading...")



# Main settings handling function
def open_settings():
    global volume, brightness, contrast, settings_open
    settings = [
        {"name": "Volume", "value": volume, "min": 0.0, "max": 1.0, "step": 0.1},
        {"name": "Brightness", "value": brightness, "min": 0.0, "max": 1.0, "step": 0.1},
        {"name": "Contrast", "value": contrast, "min": 0.0, "max": 1.0, "step": 0.1},
    ]
    selected_index = 0
    settings_open = True

    while settings_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings_open = False
                if event.key == pygame.K_w:
                    selected_index = (selected_index - 1) % len(settings)
                if event.key == pygame.K_s:
                    selected_index = (selected_index + 1) % len(settings)
                if event.key == pygame.K_d:
                    settings[selected_index]["value"] = min(settings[selected_index]["value"] + settings[selected_index]["step"], settings[selected_index]["max"])
                if event.key == pygame.K_a:
                    settings[selected_index]["value"] = max(settings[selected_index]["value"] - settings[selected_index]["step"], settings[selected_index]["min"])

        # Update settings values
        volume = settings[0]["value"]
        brightness = settings[1]["value"]
        contrast = settings[2]["value"]

        # Update volume for all sounds
        pickup_sound.set_volume(volume)
        level_up_sound.set_volume(volume)
        gambling_sound.set_volume(volume)
        pickup_sound_regen.set_volume(volume)
        fireball_sound_1.set_volume(volume)
        fireball_sound_2.set_volume(volume)
        fireball_sound_3.set_volume(volume)
        fireball_sound_4.set_volume(volume)
        fireball_sound_5.set_volume(volume)
        fireball_sound_6.set_volume(volume)
        fireball_sound_7.set_volume(volume)
        explosion_sound.set_volume(volume)
        explooosion_sound.set_volume(volume)
        screen.fill(BLACK)
        draw_tiles(0, 0)

        for i, setting in enumerate(settings):
            color = YELLOW if i == selected_index else WHITE
            setting_text = menu_font.render(f"{setting['name']}: {int(setting['value'] * 100)}%", True, color)
            screen.blit(setting_text, (width // 2 - setting_text.get_width() // 2, height // 2 - 50 + i * 40))

        pygame.display.flip()
        clock.tick(FPS)


def quit_game():
    print("Quitting game...")
    save()
    pygame.quit()
    sys.exit()


def show_victory_screen():
    victory_font = pygame.font.SysFont('Avenir', 50)
    victory_text = victory_font.render("Victory!", True, YELLOW)
    sub_text = menu_font.render("Press ESC to Exit", True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save()
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        draw_tiles(0, 0)

        text_rect = victory_text.get_rect(center=(width // 2, height // 2))
        sub_text_rect = sub_text.get_rect(center=(width // 2, height // 2 + 60))

        screen.blit(victory_text, text_rect)
        screen.blit(sub_text, sub_text_rect)

        pygame.display.flip()
        clock.tick(FPS)

def show_death_screen():
    death_font = pygame.font.Font("fonts/OptimusPrinceps.ttf", 50)
    sub_font = pygame.font.Font("fonts/OptimusPrinceps.ttf", 20)
    death_text = death_font.render("YOU DIED", True, RED)
    sub_text = sub_font.render("Press ESC to Exit", True, WHITE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        screen.fill(BLACK)

        text_rect = death_text.get_rect(center=(width // 2, height // 2))
        sub_text_rect = sub_text.get_rect(center=(width // 2, height // 2 + 45))

        screen.blit(death_text, text_rect)
        screen.blit(sub_text, sub_text_rect)

        pygame.display.flip()
        clock.tick(FPS)



# Main menu handling function
def open_menu():
    global paused, settings_open
    options = [
        {"name": "Continue"},
        {"name": "Settings"},
        {"name": "Quit"},
    ]

    selected_index = 0
    menu_open = True

    while menu_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    selected_index = (selected_index - 1) % len(options)
                if event.key == pygame.K_s:
                    selected_index = (selected_index + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    if selected_index == 0:  # Continue
                        paused = False
                        menu_open = False
                    elif selected_index == 1:  # Settings
                        open_settings()
                        settings_open = False  # Ensure the settings menu state is reset
                    elif selected_index == 2:  # Quit
                        save()
                        pygame.quit()
                        sys.exit()

        screen.fill((0, 0, 0))
        draw_tiles(0, 0)

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_index else (255, 255, 255)
            option_text = menu_font.render(option["name"], True, color)
            screen.blit(option_text, (width // 2 - option_text.get_width() // 2, height // 2 - 50 + i * 40))

        pygame.display.flip()
        clock.tick(60)

music.play(-1)

main_menu = True
while main_menu:
    cursor_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button
                right_mouse_button_pressed = False
    if pygame.mouse.get_pressed()[0] and current_fireball_cooldown == 0:
        centered_x, centered_y = player_x + player_width // 2-25, player_y + player_height // 4
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - centered_y, mouse_x - centered_x)
        shoot_forwards(centered_x, centered_y, bullet_speed, angle, bullets)
        current_fireball_cooldown = base_fireball_cooldown  # Reset the cooldown
        fireball_sound_1.play()

    if current_fireball_cooldown > 0:
        current_fireball_cooldown -= 1

    screen.fill(BLACK)
    draw_tiles(0, 0)
    screen.blit(scaled_title_image, title_rect)
    screen.blit(play_button_image, play_button_rect)
    screen.blit(settings_button_image, settings_button_rect)
    screen.blit(quit_button_image, quit_button_rect)

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
    handle_bullet_collisions(bullets, settings_button_rect, open_main_settings)
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
            save()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused  # Toggle pause state
                open_menu()

            if event.key == pygame.K_g:
                gambling_mode = True
                print("You are now gambling!!")

            if show_upgrade_menu:  # Handle upgrade selection
                if event.key == pygame.K_RETURN and upgrades==0:
                    upgrades=1  # Apply the first fireball upgrade
                    show_upgrade_menu = False
                    paused = False  # Unpause the game after selecting the upgrade
                elif event.key == pygame.K_RETURN and upgrades == 1:
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
        center_x = player_x + player_width / 2
        center_y = player_y + player_height / 4

        # Calculate camera offset
        camera_offset_x = width // 2 - player_x
        camera_offset_y = height // 2 - player_y

        # Check for right mouse button press
        if pygame.mouse.get_pressed()[2] and not paused and not show_upgrade_menu and explosion_cooldown <= 0:
            if not right_mouse_button_pressed:
                right_mouse_button_pressed = True
                cursor_x, cursor_y = pygame.mouse.get_pos()
                spawn_explosion(cursor_x, cursor_y, camera_offset_x, camera_offset_y)
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
        bullets = [bullet for bullet in bullets if
                   player_x - width // 2 < bullet['x'] < player_x + width // 2 and player_y - height // 2 < bullet[
                       'y'] < player_y + height // 2]

        # Spawn new enemies randomly
        if random.randint(0, 100) < 3:
            spawn_enemy(player_x, player_y)
        if kills > 100 and not corruption and random.randint(69, 70) == 69:
            spawn_crashing_enemy(player_x, player_y)
        if kills >= 50 and not bulky_spawned and not corruption:
            spawn_bulky(player_x, player_y)
        if kills >= 50 and corruption and not corrupty_spawned:
            spawn_corrupty(player_x, player_y)

        # Update enemy positions and check for collisions with the player
        for crashing_enemy in crashing_enemies:
            fak_x, fak_y = player_pos_on_screen
            distance_y, distance_x = fak_y- crashing_enemy.y, fak_x-crashing_enemy.x  # Calculate the vertical distance between player and enemy
            #distance_x = player_x - crashing_enemy.x  # Calculate the horizontal distance between player and enemy

            # Calculate the angle between the player and the enemy
            angle = math.atan2(distance_y, distance_x)

            # Calculate the movement components based on the angle and enemy speed
            move_x = ENEMY_SPEED * math.cos(angle)
            move_y = ENEMY_SPEED * math.sin(angle)

            # Update enemy position
            crashing_enemy.x += move_x
            crashing_enemy.y += move_y

            if (player_x-25 < crashing_enemy.x + crashing_enemy.width and player_x-25 + player_width > crashing_enemy.x and
                    player_y < crashing_enemy.y + crashing_enemy.height and player_y + player_height > crashing_enemy.y):
                if i_frames_counter == i_frames:
                    player_hp -= 5
                    i_frames_counter = 0
            # Check for collisions with bullets
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet['x'] - 5, bullet['y'] - 5, 10, 10)
                enemy_rect = pygame.Rect(crashing_enemy.x, crashing_enemy.y, crashing_enemy.width,
                                         crashing_enemy.height)

                if bullet_rect.colliderect(enemy_rect):
                    crashing_enemy.hp -= BULLET_DAMAGE
                    bullets.remove(bullet)

                    if crashing_enemy.hp <= 0:
                        crashing_enemies.remove(crashing_enemy)
                        corruption = True
                        kills = 0
                        save()
                        sys.exit("The corruption is spreading...")
        for enemy in enemies:
            # Calculate the center coordinates of the player
            player_x_center = player_x + player_width / 2
            player_y_center = player_y + player_height / 2

            # Calculate the vertical and horizontal distance between the enemy and the player's center
            distance_y = player_y_center - enemy.y
            distance_x = player_x_center - enemy.x

            # Calculate the angle between the player and the enemy
            angle = math.atan2(distance_y, distance_x)
            move_x = scaled_speed * math.cos(angle)
            move_y = scaled_speed * math.sin(angle)

            # Update enemy position
            if not enemy.death_animation_playing:
                enemy.x += move_x
                enemy.y += move_y

            # Check for collisions with the player
            Amogux, Amoguy = player_pos_on_screen
            if (player_x-25 < enemy.x + enemy.width and player_x-25 + player_width > enemy.x and
                    player_y < enemy.y + enemy.height and player_y + player_height > enemy.y):
                if i_frames_counter == i_frames:
                    player_hp -= 5
                    i_frames_counter = 0

            # Check for collisions with bullets
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet['x'] - 5, bullet['y'] - 5, 10, 10)
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

                if bullet_rect.colliderect(enemy_rect):
                    enemy.hp -= BULLET_DAMAGE

                    if enemy.hp <= 0:
                        enemy.death_animation_playing = True  # Trigger death animation
                        if upgrades <= 5:
                            bullets.remove(bullet)
                        break
                    elif enemy.hp > 0:
                        enemy.hit_animation_playing = True  # Trigger hit animation
                        bullets.remove(bullet)

        for bulky in bulkies:
            # Calculate the center coordinates of the player
            player_x_center = player_x + player_width / 2
            player_y_center = player_y + player_height / 2

            # Calculate the vertical and horizontal distance between the enemy and the player's center
            distance_y = player_y_center - bulky.y
            distance_x = player_x_center - bulky.x

            # Calculate the angle between the player and the enemy
            angle = math.atan2(distance_y, distance_x)
            move_x = bulky.speed * math.cos(angle)
            move_y = bulky.speed * math.sin(angle)

            # Update enemy position
            if not bulky.death_animation_playing:
                bulky.x += move_x
                bulky.y += move_y

            # Check for collisions with the player
            if (player_x-25 < bulky.x + bulky.width and player_x-25 + player_width > bulky.x and
                    player_y < bulky.y + bulky.height and player_y + player_height > bulky.y):
                if i_frames_counter == i_frames:
                    player_hp -= 5
                    i_frames_counter = 0

            # Check for collisions with bullets
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet['x'] - 5, bullet['y'] - 5, 10, 10)
                bulky_rect = pygame.Rect(bulky.x, bulky.y, bulky.width, bulky.height)

                if bullet_rect.colliderect(bulky_rect):
                    bulky.hp -= BULLET_DAMAGE

                    if bulky.hp <= 0:
                        bulky.death_animation_playing = True  # Trigger death animation
                        if upgrades <= 5:
                            bullets.remove(bullet)
                        break
                    elif bulky.hp > 0:
                        bullets.remove(bullet)
        for corrupty in corrupties:
            # Calculate the center coordinates of the player
            player_x_center = player_x + player_width / 2
            player_y_center = player_y + player_height / 2

            # Calculate the vertical and horizontal distance between the enemy and the player's center
            distance_y = player_y_center - corrupty.y
            distance_x = player_x_center - corrupty.x

            # Calculate the angle between the player and the enemy
            angle = math.atan2(distance_y, distance_x)
            move_x = corrupty.speed * math.cos(angle)
            move_y = corrupty.speed * math.sin(angle)

            # Update enemy position
            corrupty.x += move_x
            corrupty.y += move_y

            # Check for collisions with the player
            if (player_x-25 < corrupty.x + corrupty.width and player_x-25 + player_width > corrupty.x and
                    player_y < corrupty.y + corrupty.height and player_y + player_height > corrupty.y):
                if i_frames_counter == i_frames:
                    player_hp -= 5
                    i_frames_counter = 0

            # Check for collisions with bullets
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet['x'] - 5, bullet['y'] - 5, 10, 10)
                corrupty_rect = pygame.Rect(corrupty.x, corrupty.y, corrupty.width, corrupty.height)

                if bullet_rect.colliderect(corrupty_rect):
                    corrupty.hp -= BULLET_DAMAGE
                    bullets.remove(bullet)

                    if corrupty.hp <= 0:
                        corrupties.remove(corrupty)
                        active_exp_orbs.append({'size': enemy_exp * 5, 'x': corrupty.x, 'y': corrupty.y, 'value': enemy_exp})
                        enemy_exp = random.randint(1, 5)
                        print("You've freed us all!!")
                        show_victory_screen()
                        kills += 1
        if player_hp <= 0:
            upgrades = 0
            kills = 0
            player_hp = 100
            exp = 0
            player_level = 1
            corruption = False
            current_max_exp = 30
            save()
            show_death_screen()

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

    enemies_to_remove = []
    for enemy in enemies:
        if enemy.hit_animation_playing and not enemy.death_animation_playing:
            enemy.hit_frame_count += 1
            if enemy.hit_frame_count % 4 == 0 and not paused and not show_upgrade_menu:  # Adjust frame rate of hit animation here
                enemy.hit_frame = enemy.hit_frame + 1

            # Check if hit animation duration is over
            if enemy.hit_frame >= len(hit_enemy_frames):
                enemy.hit_animation_playing = False
                enemy.hit_frame_count = 0

        elif enemy.death_animation_playing:
            enemy.death_frame_count += 1
            if enemy.death_frame_count % 4 == 0 and not paused and not show_upgrade_menu:  # Adjust frame rate of hit animation here
                enemy.death_frame = enemy.death_frame + 1

            # Check if death animation duration is over
            if enemy.death_frame >= len(death_enemy_frames):  # Ensure the death animation has completed
                enemies_to_remove.append(enemy)
                active_exp_orbs.append({'size': enemy_exp * 5, 'x': enemy.x, 'y': enemy.y, 'value': enemy_exp})
                enemy_exp = random.randint(1, 5)
                kills += 1
                if random.randint(1, 100) == 69:
                    active_regen_orbs.append({'x': enemy.x, 'y': enemy.y, 'size': regen_orb_size, 'value': regen_amount})
                    print("A wild regen orb spawned!!!!!")
            else:
                # Display the current frame of the death animation
                enemy_image = death_enemy_frames[enemy.death_frame]
                if enemy.x > player_x:
                    enemy_image = pygame.transform.flip(enemy_image, True, False)
                screen.blit(enemy_image, (enemy.x + camera_offset_x, enemy.y + camera_offset_y))
                continue  # Skip the rest of the loop to ensure no other animation is played

        else:
            enemy.frame_count += 1
            if enemy.frame_count % 6 == 0 and not paused and not show_upgrade_menu:
                enemy.frame = (enemy.frame + 1) % len(enemy_frames)

        # Choose the appropriate frame to display if not in death animation
        if not enemy.death_animation_playing:
            if enemy.hit_animation_playing:
                if enemy.x > player_x:
                    enemy_image = pygame.transform.flip(hit_enemy_frames[enemy.hit_frame], True, False)
                else:
                    enemy_image = hit_enemy_frames[enemy.hit_frame]
            else:
                if enemy.x > player_x:
                    enemy_image = pygame.transform.flip(enemy_frames[enemy.frame], True, False)
                else:
                    enemy_image = enemy_frames[enemy.frame]

            screen.blit(enemy_image, (enemy.x + camera_offset_x, enemy.y + camera_offset_y))
    # Remove enemies marked for removal after the loop
    for enemy in enemies_to_remove:
        enemies.remove(enemy)
    bulkies_to_remove = []
    for bulky in bulkies:
        if bulky.death_animation_playing:
            bulky.death_frame_count += 1
            if bulky.death_frame_count % 4 == 0 and not paused and not show_upgrade_menu:
                bulky.death_frame = bulky.death_frame + 1

            if bulky.death_frame >= len(bulky_death_frames) - 1:  # Ensure the death animation has completed
                bulkies_to_remove.append(bulky)
                active_exp_orbs.append({'size': enemy_exp * 2, 'x': bulky.x, 'y': bulky.y, 'value': enemy_exp})
                enemy_exp = random.randint(30, 50)
                kills += 1

            else:
                # Display the current frame of the death animation
                bulky_image = bulky_death_frames[bulky.death_frame]
                if bulky.x > player_x:
                    bulky_image = pygame.transform.flip(bulky_image, True, False)
                screen.blit(bulky_image, (bulky.x + camera_offset_x, bulky.y + camera_offset_y))
                continue  # Skip the rest of the loop to ensure no other animation is played
        else:
            # Animate and draw bulky enemy
            bulky.frame_count += 1
            if bulky.frame_count % 10 == 0 and not paused and not show_upgrade_menu:  # Adjust frame rate of animation here
                bulky.frame = (bulky.frame + 1) % len(bulky_frames)

            if bulky.x > player_x:
                # Enemy is coming from the left side of the screen, flip the sprite
                bulky_image = pygame.transform.flip(bulky_frames[bulky.frame], True, False)
            else:
                # Enemy is coming from the right side of the screen, use the original sprite
                bulky_image = bulky_frames[bulky.frame]

            screen.blit(bulky_image, (bulky.x + camera_offset_x, bulky.y + camera_offset_y))

    for bulky in bulkies_to_remove:
        bulkies.remove(bulky)

    for crashing_enemy in crashing_enemies:
        crashing_enemy.frame_count += 1
        if crashing_enemy.frame_count % 5 == 0 and not paused and not show_upgrade_menu:
            crashing_enemy.frame = (crashing_enemy.frame + 1) % len(crashing_enemy_frames)

        if crashing_enemy.x > player_x:
            # Enemy is coming from the left side of the screen, flip the sprite
            crashing_enemy_image = pygame.transform.flip(crashing_enemy_frames[crashing_enemy.frame], True, False)
        else:
            # Enemy is coming from the right side of the screen, use the original sprite
            crashing_enemy_image = crashing_enemy_frames[crashing_enemy.frame]

        # Scale the image to the size defined by corrupty.height and corrupty.width
        crashing_enemy_image = pygame.transform.scale(crashing_enemy_image, (crashing_enemy.width, crashing_enemy.height))

        screen.blit(crashing_enemy_image, (crashing_enemy.x + camera_offset_x, crashing_enemy.y + camera_offset_y))

    for corrupty in corrupties:
        corrupty.frame_count += 1
        if corrupty.frame_count % 6 == 0 and not paused and not show_upgrade_menu:
            corrupty.frame = (corrupty.frame + 1) % len(corrupty_frames)

        if corrupty.x > player_x:
            # Enemy is coming from the left side of the screen, flip the sprite
            corrupty_image = pygame.transform.flip(corrupty_frames[corrupty.frame], True, False)
        else:
            # Enemy is coming from the right side of the screen, use the original sprite
            corrupty_image = corrupty_frames[corrupty.frame]

        # Scale the image to the size defined by corrupty.height and corrupty.width
        corrupty_image = pygame.transform.scale(corrupty_image, (corrupty.width, corrupty.height))

        screen.blit(corrupty_image, (corrupty.x + camera_offset_x, corrupty.y + camera_offset_y))

    for bullet in bullets:
        # Calculate angle of rotation based on bullet's velocity
        angle = math.atan2(-bullet['dy'], bullet['dx'])  # Use negative y-velocity to account for inverted y-axis

        # Rotate the bullet image
        rotated_bullet_image = pygame.transform.rotate(bullet_image, math.degrees(angle))

        # Draw the rotated bullet image at the bullet's position
        screen.blit(rotated_bullet_image, (
            bullet['x'] - rotated_bullet_image.get_width() / 2 + camera_offset_x, bullet['y'] - rotated_bullet_image.get_height() / 2 + camera_offset_y))
    if explosion:
        if explosion_frame_index < len(explosion_frames):
            screen.blit(explosion_frames[explosion_frame_index],
                        (explosion_x - 50 + camera_offset_x, explosion_y - 50 + camera_offset_y))
            explosion_frame_duration -= 1
            if explosion_frame_duration <= 0:
                explosion_frame_index += 1
                explosion_frame_duration = 4  # Reset frame duration
            # Check for collisions with the explosion
            check_explosion_collisions(explosion_x, explosion_y)
        else:
            explosion = False  # End explosion animation

    if explosion_cooldown > 0 and not paused and not show_upgrade_menu:
        explosion_cooldown -= 1

    draw_hp_bar()  # Draw the player's HP bar
    draw_exp_bar()  # Draw the experience bar
    draw_kill_counter(kills)
    draw_coordinates(player_x, player_y)
    draw_explosion_cooldown(explosion_cooldown)
    if rendering == "right":
        screen.blit(frames_right[current_frame], (player_pos_on_screen))  # Draw the current frame of player sprite
    if rendering == "up":
        screen.blit(frames_up[current_frame], (player_pos_on_screen))
    if rendering == "left":
        screen.blit(frames_left[current_frame], (player_pos_on_screen))
    if rendering == "down":
        screen.blit(frames_down[current_frame], (player_pos_on_screen))
    if i_frames_counter < i_frames:
        i_frames_counter += 1
    if exp >= current_max_exp:
        level_up()
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