import pygame
import sys
import random
from base_enemy import Enemy
from crashing_enemy import CrashingEnemy
import math

class Game:
    def __init__(self):
        # Set up the game window
        fullscreen = False  # Change this variable to switch between fullscreen and windowed mode

        if fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen_width = 690  # Fanny number
            screen_height = 690  # Fanny number
            screen = pygame.display.set_mode((screen_width, screen_height))

        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.FPS = 60
        self.tile_image = pygame.image.load('sprites/tile.png')
        self.original_tile_size = 476
        self.tile_size = 64
        self.scaled_tile_image = pygame.transform.scale(self.tile_image, (self.tile_size, self.tile_size))

        # Load sprite sheet for the character walking to the right
        self.sprite_sheet_path_right = 'sprites/Niko_right.png'
        self.sprite_sheet_path_up = 'sprites/Niko_up.png'
        self.sprite_sheet_path_down = 'sprites/Niko_down.png'
        self.sprite_sheet_path_left = 'sprites/Niko_left.png'
        self.sprite_sheet_right = pygame.image.load(self.sprite_sheet_path_right).convert_alpha()
        self.sprite_sheet_up = pygame.image.load(self.sprite_sheet_path_up).convert_alpha()
        self.sprite_sheet_down = pygame.image.load(self.sprite_sheet_path_down).convert_alpha()
        self.sprite_sheet_left = pygame.image.load(self.sprite_sheet_path_left).convert_alpha()

        # Frame setup
        self.frame_width, self.frame_height = 24, 30
        self.frames_up = [pygame.transform.scale(
            self.sprite_sheet_up.subsurface(pygame.Rect(self.frame_width * i, 0, self.frame_width, self.frame_height)), (48, 60)) for i in
                     range(3)]
        self.frames_right = [pygame.transform.scale(
            self.sprite_sheet_right.subsurface(pygame.Rect(self.frame_width * i, 0, self.frame_width, self.frame_height)), (48, 60)) for i
                        in range(3)]
        self.frames_down = [pygame.transform.scale(
            self.sprite_sheet_down.subsurface(pygame.Rect(self.frame_width * i, 0, self.frame_width, self.frame_height)), (48, 60)) for i in
                       range(3)]
        self.frames_left = [pygame.transform.scale(
            self.sprite_sheet_left.subsurface(pygame.Rect(self.frame_width * i, 0, self.frame_width, self.frame_height)), (48, 60)) for i in
                       range(3)]
        self.current_frame = 0
        self.frame_count = 0
        self.rendering = "down"

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Player attributes
        self.player_x = self.width // 2
        self.player_y = self.height // 2
        self.player_speed = 5
        self.player_height = self.frame_width
        self.player_width = self.frame_height
        self.player_hp = 100
        self.invince_frames = 10
        self.i_frame_temp = self.invince_frames
        self.kills = 0

        # Experience system
        self.exp = 0
        self.enemy_exp = 0
        self.active_exp_orbs = []
        self.current_max_exp = 30
        self.max_level = 1000  # for ending
        self.player_level = 1  # keeping track of the player's current level
        self.exp_increase_per_level = 5
        self.levelling = False

        # Bullet attributes
        self.bullets = []
        self.bullet_speed = 10

        # Recoil attributes
        self.recoil_strength = 0  # Adjust this value to control the strength of the recoil
        self.recoil_duration = 0  # Adjust this value to control how long the recoil effect lasts
        self.recoil_counter = 0

        self.base_enemy_exp = random.randint(1, 5)

        self.ENEMY_SPEED = 0.5  # Adjust this value as needed

        self.paused = False

        # Gun variables
        self.base_gun_cooldown = 2
        self.base_sword_cooldown = 1

        # definitions
        def draw_tiles():
            for y in range(0, self.height, self.tile_size):
                for x in range(0, self.width, self.tile_size):
                    screen.blit(self.scaled_tile_image, (x, y))

        def shoot_base_gun(player_x, player_y, bullets, bullet_speed, recoil_strength):
            mouseX, mouseY = pygame.mouse.get_pos()
            angle = math.atan2(mouseY - player_y, mouseX - player_x)
            bullets.append([player_x, player_y, bullet_speed * math.cos(angle), bullet_speed * math.sin(angle)])
            # Apply recoil when shooting
            player_x -= recoil_strength * math.cos(angle)
            player_y -= recoil_strength * math.sin(angle)

        def draw_kill_counter(kills):
            font = pygame.font.Font(None, 24)
            kills_text = font.render(f"Kills: {kills}", True, self.RED)
            text_width, text_height = font.size(f"Kills: {kills}")
            text_x = (self.width - text_width) // 3
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
            exp_bar_width = self.width - 20  # Define the width of the experience bar
            exp_bar_height = 20
            exp_indicator_width = int(exp / max_exp * exp_bar_width)  # Calculate the width of the experience indicator

            pygame.draw.rect(screen, self.BLUE, (10, 10, exp_bar_width, exp_bar_height))  # Blue background
            pygame.draw.rect(screen, self.GREEN, (10, 10, exp_indicator_width, exp_bar_height))  # Green indicator

            font = pygame.font.Font(None, 24)
            exp_text = font.render(f"EXP: {exp}/{max_exp}", True, self.WHITE)
            text_width, text_height = font.size(f"EXP: {exp}/{max_exp}")
            text_x = (self.width - text_width) // 2
            text_y = exp_bar_height + 20
            screen.blit(exp_text, (text_x, text_y))

        # Function to spawn enemies
        def spawn_enemy():
            spawn_side = random.randint(0, 3)
            if spawn_side == 0:
                enemy_x = random.randint(0, self.width)
                enemy_y = self.height + 20
            elif spawn_side == 1:
                enemy_x = random.randint(0, self.width)
                enemy_y = -self.height - 20
            elif spawn_side == 2:
                enemy_x = -self.width - 20
                enemy_y = random.randint(0, self.height)
            else:
                enemy_x = self.width + 20
                enemy_y = random.randint(0, self.height)

            basic_enemy = Enemy(enemy_x, enemy_y, 20, 20, 10, self.ENEMY_SPEED)
            self.enemies.append(basic_enemy)

        # Function to spawn enemies
        def spawn_crashing_enemy():
            spawn_side = random.randint(0, 3)
            if spawn_side == 0:
                enemy_x = random.randint(0, self.width)
                enemy_y = self.height + 20
            elif spawn_side == 1:
                enemy_x = random.randint(0, self.width)
                enemy_y = -self.height - 20
            elif spawn_side == 2:
                enemy_x = -self.width - 20
                enemy_y = random.randint(0, self.height)
            else:
                enemy_x = self.width + 20
                enemy_y = random.randint(0, self.height)
            crashingenemy = CrashingEnemy(enemy_x, enemy_y, 20, 20, 10, self.ENEMY_SPEED)
            self.crashing_enemies.append(crashingenemy)

        # Function to draw player's health bar
        def draw_hp_bar():
            hp_bar_width = self.player_hp * 2
            hp_bar_height = 20
            hp_indicator_width = int(self.player_hp / 100 * hp_bar_width)

            pygame.draw.rect(screen, self.RED, (10, self.height - 30, hp_bar_width, hp_bar_height))  # Red background
            pygame.draw.rect(screen, self.GREEN, (10, self.height - 30, hp_indicator_width, hp_bar_height))  # Green indicator
            font = pygame.font.Font(None, 36)
            hp_text = font.render(f"{self.player_hp}/100 HP", True, self.WHITE)
            screen.blit(hp_text, (220, self.height - 30))

    def run(self):
        # Game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if pygame.mouse.get_pressed()[0]:
                    self.shoot_base_gun(self.player_x, self.player_y, self.bullets, self.bullet_speed, self.recoil_strength)

            if not self.paused:  # Only update game state if not paused
                # Update player input and game state
                global crashing_enemy
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.player_x -= self.player_speed
                    self.frame_count += 1
                    if self.frame_count % 2 == 0:  # Adjust frame rate of animation here
                        current_frame = (self.current_frame + 1) % len(self.frames_left)
                    rendering = "left"
                if keys[pygame.K_d]:
                    self.player_x += self.player_speed
                    self.frame_count += 1
                    if self.frame_count % 2 == 0:  # Adjust frame rate of animation here
                        current_frame = (self.current_frame + 1) % len(self.frames_right)
                    rendering = "right"
                if keys[pygame.K_w]:
                    self.player_y -= self.player_speed
                    self.frame_count += 1
                    if self.frame_count % 2 == 0:
                        current_frame = (self.current_frame + 1) % len(self.frames_up)
                    rendering = "up"
                if keys[pygame.K_s]:
                    self.player_y += self.player_speed
                    self.frame_count += 1
                    if self.frame_count % 2 == 0:  # Adjust frame rate of animation here
                        current_frame = (self.current_frame + 1) % len(self.frames_down)
                    rendering = "down"

                # Update bullet positions and remove bullets that go off-screen
                for bullet in self.bullets:
                    bullet[0] += bullet[2]
                    bullet[1] += bullet[3]

                bullets = [bullet for bullet in self.bullets if 0 <= bullet[0] <= self.width and 0 <= bullet[1] <= self.height]

                # Spawn new enemies randomly
                if random.randint(0, 100) < 5:
                    self.spawn_enemy()
                elif random.randint(0, 1000) == 69:
                    self.spawn_crashing_enemy()

                # Update enemy positions and check for collisions with the player
                for crashing_enemy in self.crashing_enemies:
                    distance_y = self.player_y - crashing_enemy.y  # Calculate the vertical distance between player and enemy
                    distance_x = self.player_x - crashing_enemy.x  # Calculate the horizontal distance between player and enemy

                    # Calculate the angle between the player and the enemy
                    angle = math.atan2(distance_y, distance_x)

                    # Calculate the movement components based on the angle and enemy speed
                    move_x = self.ENEMY_SPEED * math.cos(angle)
                    move_y = self.ENEMY_SPEED * math.sin(angle)

                    # Update enemy position
                    crashing_enemy.x += move_x
                    crashing_enemy.y += move_y

                    # Check for collisions with the player
                    if (
                            self.player_x < crashing_enemy.x + crashing_enemy.width and self.player_x + self.player_width > crashing_enemy.x and
                            self.player_y < crashing_enemy.y + crashing_enemy.height and self.player_y + self.player_height > crashing_enemy.y):
                        if self.invince_frames == self.i_frame_temp:
                            self.player_hp -= 5
                            self.invince_frames = 0

                    # Check for collisions with bullets
                    for bullet in bullets:
                        bullet_rect = pygame.Rect(bullet[0] - 5, bullet[1] - 5, 10, 10)
                        enemy_rect = pygame.Rect(crashing_enemy.x, crashing_enemy.y, crashing_enemy.width,
                                                 crashing_enemy.height)

                        if bullet_rect.colliderect(enemy_rect):
                            crashing_enemy.hp -= 10
                            bullets.remove(bullet)

                            if crashing_enemy.hp <= 0:
                                sys.exit()

                for enemy in self.enemies:
                    distance_y = self.player_y - enemy.y  # Calculate the vertical distance between player and enemy
                    distance_x = self.player_x - enemy.x  # Calculate the horizontal distance between player and enemy

                    # Calculate the angle between the player and the enemy
                    angle = math.atan2(distance_y, distance_x)

                    # Calculate the movement components based on the angle and enemy speed
                    move_x = self.ENEMY_SPEED * math.cos(angle)
                    move_y = self.ENEMY_SPEED * math.sin(angle)

                    # Update enemy position
                    enemy.x += move_x
                    enemy.y += move_y

                    # Check for collisions with the player
                    if (self.player_x < enemy.x + enemy.width and self.player_x + self.player_width > enemy.x and
                            self.player_y < enemy.y + enemy.height and self.player_y + self.player_height > enemy.y):
                        if self.invince_frames == self.i_frame_temp:
                            self.player_hp -= 5
                            invince_frames = 0

                    # Check for collisions with bullets
                    for bullet in bullets:
                        bullet_rect = pygame.Rect(bullet[0] - 5, bullet[1] - 5, 10, 10)
                        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

                        if bullet_rect.colliderect(enemy_rect):
                            enemy.hp -= 10
                            bullets.remove(bullet)

                            if enemy.hp <= 0:
                                self.enemies.remove(enemy)
                                self.active_exp_orbs.append(
                                    {'size': self.enemy_exp * 3, 'x': enemy.x, 'y': enemy.y, 'value': self.enemy_exp})
                                enemy_exp = random.randint(1, 5)
                                self.kills += 1

                if self.player_hp <= 0:
                    sys.exit()

                # Check for collisions between player and exp orbs
                for exp_orb in self.active_exp_orbs:
                    orb_center_x = exp_orb['x']
                    orb_center_y = exp_orb['y']
                    orb_radius = exp_orb['size']
                    orb_exp = exp_orb['value']  # Extract the exp value associated with the orb

                    # Calculate the distance between player and exp orb's center
                    distance_to_orb = math.sqrt((self.player_x - orb_center_x) ** 2 + (self.player_y - orb_center_y) ** 2)

                    # Check if the player collides with the exp orb
                    if distance_to_orb < orb_radius + self.player_width / 2:
                        # Player gains exp equal to the amount associated with the exp orb
                        self.exp += orb_exp
                        # Remove the exp orb from the active list
                        self.active_exp_orbs.remove(exp_orb)

            # Add code to handle pausing the game
            if self.paused:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.paused = False
                    self.paused = False

                pygame.time.Clock().tick(60)  # Limit frame rate to reduce CPU usage



