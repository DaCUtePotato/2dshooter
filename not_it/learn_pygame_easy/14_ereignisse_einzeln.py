import pygame # Packet laden
import sys
import random


pygame.init() # Muss immer bei der Verwendung von Pygame am Anfang gemacht werden zur internen Initialisierung

# Fenstergrösse definieren
width = 900
height = 500
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Mein Erstes Pygame Programm")

# Farben definieren mit RGB Wert
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)

# Zeitmesser einführen
clock = pygame.time.Clock()

# Raumschiff Koordinaten
gelb_x = 100
gelb_y = 200
rot_x = 400
rot_y = 200

# Raumschiff Eigenschaften
vel = 5 # Geschwindigkeit (engl. velocity)

# Bilder hinzufügen
gelbes_raumschiff = pygame.image.load("./bilder_und_ton/spaceship_yellow.png")
gelbes_raumschiff = pygame.transform.scale(gelbes_raumschiff, (55, 40))
gelbes_raumschiff = pygame.transform.rotate(gelbes_raumschiff, 90) # 90 grad rotieren
rotes_raumschiff = pygame.image.load("./bilder_und_ton/spaceship_red.png")
rotes_raumschiff = pygame.transform.scale(rotes_raumschiff, (55, 40))
rotes_raumschiff = pygame.transform.rotate(rotes_raumschiff, 270) # 270 grad rotieren

# Bewegendes Rechteck
rechteck_x = 200
rechteck_y = 200
rechteck_breite = 80
rechteck_hoehe = 80
rechteck_vel_x = 1
rechteck_vel_y = 1
rechteck = pygame.Rect(rechteck_x, rechteck_y, rechteck_breite, rechteck_hoehe)

# Bullets
bullets = [] # Liste an bullets
bullet_vel = ... # todo: bullet Geschwindigkeit bestimmen

while True:
    for event in pygame.event.get():
        # If the player clicks the red 'x', it is considered a quit event
        if event.type == pygame.QUIT:
            pygame.quit() # Gegenteil von pygame.init()
            sys.exit() # Programm regulär beenden

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # todo: bullet kreieren und einer Liste an bullets hinzufügen

    screen.fill(yellow)

    # todo: bullets bewegen

    # Rechteck bewegen
    dir_change_x = random.gauss(0, 0.1)
    dir_change_y = random.gauss(0, 0.1)
    rechteck_vel_x = rechteck_vel_x + dir_change_x
    rechteck_vel_y = rechteck_vel_y + dir_change_y
    rechteck.x = rechteck.x + rechteck_vel_x
    rechteck.y = rechteck.y + rechteck_vel_y


    # Überprüfe, ob Taste gedrückt wurde
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_a]: # überprüfe, ob Taste 'a' gedrückt wurde
        gelb_x = gelb_x - vel
    if keys_pressed[pygame.K_d]: # überprüfe, ob Taste 'd' gedrückt wurde
        gelb_x = gelb_x + vel
    if keys_pressed[pygame.K_w]: # überprüfe, ob Taste 'w' gedrückt wurde
        gelb_y = gelb_y - vel
    if keys_pressed[pygame.K_s]: # überprüfe, ob Taste 's' gedrückt wurde
        gelb_y = gelb_y + vel

    if keys_pressed[pygame.K_LEFT]:
        rot_x = rot_x - vel
    if keys_pressed[pygame.K_RIGHT]:
        rot_x = rot_x + vel
    if keys_pressed[pygame.K_UP]:
        rot_y = rot_y - vel
    if keys_pressed[pygame.K_DOWN]:
        rot_y = rot_y + vel

    screen.blit(gelbes_raumschiff, (gelb_x, gelb_y)) # blit für Bilder und Text (surfaces)
    screen.blit(rotes_raumschiff, (rot_x, rot_y)) # blit für Bilder und Text (surfaces)

    pygame.draw.rect(screen, red, rechteck)

    # todo: bullets zeichnen

    # pygame vollständig updaten
    pygame.display.update()

    clock.tick(60) # while-Schleife soll nicht öffters als 60 mal pro Sekunde ausgeführt werden.





