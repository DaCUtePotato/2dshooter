import pygame # Packet laden
import sys

pygame.init() # Muss immer bei der Verwendung von Pygame am Anfang gemacht werden zur internen Initialisierung

# Fenstergrösse definieren
width = 400
height = 300
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Mein Erstes Pygame Programm")

# Farben definieren mit RGB Wert
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
orange = (255, 100, 0)
black = (0, 0, 0)
green = (0, 255, 0)
darkgreen = (0, 150, 0)
blue = (0, 0, 255)

# Zeitmesser einführen
clock = pygame.time.Clock()

# Rechteck-Objekt kreieren
rechteck = pygame.Rect(50, 100, 50, 100)

# Geschwindigkeit Rechteck
# Todo: Geschwindigkeit des Rechtecks bei Steuereingabe

while True:
    for event in pygame.event.get():
        # If the player clicks the red 'x', it is considered a quit event
        if event.type == pygame.QUIT:
            pygame.quit() # Gegenteil von pygame.init()
            sys.exit() # Programm regulär beenden

    screen.fill(yellow)

    # Steuerung für Rechteck
    # Todo: Steuerung Rechteck einbauen

    # Zeichne Rechteck
    pygame.draw.rect(screen, red, rechteck)

    # pygame vollständig updaten
    pygame.display.update()

    clock.tick(60) # while-Schleife soll nicht öffters als 60 mal pro Sekunde ausgeführt werden.



