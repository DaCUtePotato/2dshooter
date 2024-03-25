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

# Bilder hinzufügen
# todo: Bilder laden und skalieren/rotieren


while True:
    for event in pygame.event.get():
        # If the player clicks the red 'x', it is considered a quit event
        if event.type == pygame.QUIT:
            pygame.quit() # Gegenteil von pygame.init()
            sys.exit() # Programm regulär beenden

    screen.fill(yellow)

    # todo: Bilder hinzufügen

    # pygame vollständig updaten
    pygame.display.update()

    clock.tick(60) # while-Schleife soll nicht öffters als 60 mal pro Sekunde ausgeführt werden.



