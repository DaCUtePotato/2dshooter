import pygame # Packet laden
import sys
import random

pygame.init() # Muss immer bei der Verwendung von Pygame am Anfang gemacht werden zur internen Initialisierung

# Fenstergrösse definieren
width = 700
height = 500
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Mein Erstes Pygame Programm")

# Farben definieren mit RGB Wert
white = (255, 255, 255)
yellow = (255, 255, 0)
red = ... # Todo: restliche Farben definieren
orange = ...
black = ...
green = ...
darkgreen = ...
blue = ...

# Zeitmesser einführen
clock = pygame.time.Clock()

# Anzahl Frames
frame_count = 0

while True:
    for event in pygame.event.get():
        # If the player clicks the red 'x', it is considered a quit event
        if event.type == pygame.QUIT:
            pygame.quit() # Gegenteil von pygame.init()
            sys.exit() # Programm regulär beenden

    frame_count += 1

    # HINTERGRUND MUSS VOR DEN GEOMETRISCHEN OBJEKTEN GEZEICHNET WERDEN
    screen.fill(yellow)

    # Zeichne Grass
    # Todo: Grass zeichnen

    # Zeichne Haus
    # Todo: Haus zeichnen

    # Zeichne Sonne
    # Todo: Sonne zeichnen

    # pygame vollständig updaten
    pygame.display.update()

    clock.tick(60) # while-Schleife soll nicht öffters als 60 mal pro Sekunde ausgeführt werden.



