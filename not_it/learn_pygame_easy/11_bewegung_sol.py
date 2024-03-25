import pygame # Packet laden
import sys

pygame.init() # Muss immer bei der Verwendung von Pygame am Anfang gemacht werden zur internen Initialisierung

# Fenstergrösse definieren
width = 900
height = 500
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Mein Erstes Pygame Programm")

# Farben definieren mit RGB Wert
white = (255, 255, 255)
yellow = (255, 255, 0)

# Zeitmesser einführen
clock = pygame.time.Clock()

# Raumschiff Koordinaten
gelb_x = 100
gelb_y = 200
rot_x = 400
rot_y = 200

# Bilder hinzufügen
gelbes_raumschiff = pygame.image.load("./bilder_und_ton/spaceship_yellow.png")
gelbes_raumschiff = pygame.transform.scale(gelbes_raumschiff, (55, 40))
gelbes_raumschiff = pygame.transform.rotate(gelbes_raumschiff, 90) # 90 grad rotieren
rotes_raumschiff = pygame.image.load("./bilder_und_ton/spaceship_red.png")
rotes_raumschiff = pygame.transform.scale(rotes_raumschiff, (55, 40))
rotes_raumschiff = pygame.transform.rotate(rotes_raumschiff, 270) # 270 grad rotieren


while True:
    for event in pygame.event.get():
        # If the player clicks the red 'x', it is considered a quit event
        if event.type == pygame.QUIT:
            pygame.quit() # Gegenteil von pygame.init()
            sys.exit() # Programm regulär beenden

    screen.fill(yellow)

    gelb_x = gelb_x + 2
    rot_y = rot_y - 1

    screen.blit(gelbes_raumschiff, (gelb_x, gelb_y)) # blit für Bilder und Text (surfaces)
    screen.blit(rotes_raumschiff, (rot_x, rot_y)) # blit für Bilder und Text (surfaces)

    # pygame vollständig updaten
    pygame.display.update()

    clock.tick(60) # while-Schleife soll nicht öffters als 60 mal pro Sekunde ausgeführt werden.





