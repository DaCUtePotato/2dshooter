import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BULLET_SPEED = 8
ENEMY_SPEED = 2
RECOIL_AMOUNT = 0.25
SLIDING_FRICTION = 0.9  # Adjust the sliding friction
PARTICLE_COUNT = 30
MAX_HEALTH = 100

DEATH_SCREEN_FONT = pygame.font.Font(None, 72)
BUTTON_FONT = pygame.font.Font(None, 36)
#exp_bar_outline = pygame.Rect()

# Game state constants
GAME_RUNNING = 0
PLAYER_DIED = 1
current_game_state = GAME_RUNNING

# Set display flags for full screen
flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF

# Money system
exp = 0

# Player upgrades
selected_upgrade = None

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
pygame.display.set_caption("DaCutePotato's Shooter")

# Create the player circle
player_radius = 20
player_x = WIDTH // 2
player_y = HEIGHT // 2

# Set up player variables
player_speed = 5  # Adjust the player's speed
player_speed_x = 0
player_speed_y = 0
player_health = MAX_HEALTH

# Set up bullet variables
bullets = []
bullet_speed_upgrade = 1  # Upgrade effect on bullet speed

# Set up particle variables
particles = []
enemy_particles = []

# Set up enemy variables
enemies = []

# Pause menu variables
pause_menu_active = False

# Set up clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to reset the game state
def reset_game():
    global player_x, player_y, player_health, bullets, money, enemies
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    player_health = MAX_HEALTH
    bullets = []
    money = 0
    enemies = []

# Class definitions for Particle and EnemyParticle
class Particle:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = RED
        self.radius = random.randint(2, 5)
        self.life = random.randint(10, 30)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

def apply_upgrades():
    pass

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = (0, 0, 255)  # Blue for enemies
        self.radius = 15

    def update(self):
        # Move the enemy towards the player
        angle = math.atan2(player_y - self.y, player_x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class EnemyParticle:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = (0, 0, 255)  # Blue for enemy particles
        self.radius = random.randint(2, 5)
        self.life = random.randint(10, 30)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


# Game loop
running = True
recoil_active = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - player_y, mouse_x - player_x)
            bullet_dx = (BULLET_SPEED + bullet_speed_upgrade) * math.cos(angle)
            bullet_dy = (BULLET_SPEED + bullet_speed_upgrade) * math.sin(angle)
            bullets.append((player_x, player_y, bullet_dx, bullet_dy))
            recoil_active = True
            for _ in range(PARTICLE_COUNT):
                particle_dx = random.uniform(-1, 1)
                particle_dy = random.uniform(-1, 1)
                particles.append(Particle(player_x, player_y, particle_dx, particle_dy))
        elif event.type == pygame.MOUSEBUTTONUP:
            recoil_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_game_state == GAME_RUNNING:
                    pause_menu_active = not pause_menu_active
                elif current_game_state == PLAYER_DIED:
                    running = False  # Exit the entire game when the player dies

    if current_game_state == GAME_RUNNING:
        # Spawn enemies off-window randomly
        if random.random() < 0.02:
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                enemies.append(Enemy(random.uniform(0, WIDTH), 0, ENEMY_SPEED))
            elif side == 'bottom':
                enemies.append(Enemy(random.uniform(0, WIDTH), HEIGHT, ENEMY_SPEED))
            elif side == 'left':
                enemies.append(Enemy(0, random.uniform(0, HEIGHT), ENEMY_SPEED))
            elif side == 'right':
                enemies.append(Enemy(WIDTH, random.uniform(0, HEIGHT), ENEMY_SPEED))

        # Check for player-enemy collisions
        for enemy in enemies:
            distance = math.sqrt((player_x - enemy.x) ** 2 + (player_y - enemy.y) ** 2)
            if distance < player_radius + enemy.radius:
                # Player-enemy collision detected
                player_health -= 10  # Decrease player's health
                enemies.remove(enemy)  # Remove the enemy from the list
                for _ in range(PARTICLE_COUNT):
                    particle_dx = random.uniform(-1, 1)
                    particle_dy = random.uniform(-1, 1)
                    enemy_particles.append(EnemyParticle(enemy.x, enemy.y, particle_dx, particle_dy))

        # Check if player health drops below 0
        if player_health <= 0:
            current_game_state = PLAYER_DIED
            running = False  # Exit the entire game when the player dies

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_speed_y = -player_speed
        if keys[pygame.K_s]:
            player_speed_y = player_speed
        if keys[pygame.K_a]:
            player_speed_x = -player_speed
        if keys[pygame.K_d]:
            player_speed_x = player_speed

        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            player_speed_y *= SLIDING_FRICTION
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            player_speed_x *= SLIDING_FRICTION

        if recoil_active:
            player_speed_x -= RECOIL_AMOUNT * math.cos(angle)
            player_speed_y -= RECOIL_AMOUNT * math.sin(angle)

        player_x += player_speed_x
        player_y += player_speed_y

        bullets = [(x + dx, y + dy, dx, dy) for x, y, dx, dy in bullets]

        particles = [particle for particle in particles if particle.life > 0]
        for particle in particles:
            particle.update()

        for enemy in enemies:
            enemy.update()

        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in bullets:
            for enemy in enemies:
                distance = math.sqrt((bullet[0] - enemy.x) ** 2 + (bullet[1] - enemy.y) ** 2)
                if distance < 5 + enemy.radius:
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
#                    add_exp(enemy.x, enemy.y)
                    for _ in range(PARTICLE_COUNT):
                        particle_dx = random.uniform(-1, 1)
                        particle_dy = random.uniform(-1, 1)
                        enemy_particles.append(EnemyParticle(enemy.x, enemy.y, particle_dx, particle_dy))

        for bullet in bullets_to_remove:
            bullets.remove(bullet)

        for enemy in enemies_to_remove:
            enemies.remove(enemy)

        enemy_particles = [particle for particle in enemy_particles if particle.life > 0]
        for particle in enemy_particles:
            particle.update()

        apply_upgrades()

        screen.fill(WHITE)

        pygame.draw.circle(screen, RED, (int(player_x), int(player_y)), player_radius)

        pygame.draw.rect(screen, RED, (10, 10, player_health * 2, 20))
        pygame.draw.rect(screen, RED, (10, 10, MAX_HEALTH * 2, 20), 2)

        money_font = pygame.font.Font(None, 36)

        card_font = pygame.font.Font(None, 20)

        if selected_upgrade:
            selected_upgrade_text = card_font.render(f"Selected Upgrade: {selected_upgrade}", True, RED)
            screen.blit(selected_upgrade_text, (10, HEIGHT - 30))

        for bullet in bullets:
            pygame.draw.circle(screen, RED, (int(bullet[0]), int(bullet[1])), 5)

        for particle in particles:
            particle.draw(screen)

        for particle in enemy_particles:
            particle.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()