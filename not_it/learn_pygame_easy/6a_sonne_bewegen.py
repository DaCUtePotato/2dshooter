import pygame # Packet laden
import sys
import random

pygame.init() # Muss immer bei der Verwendung von Pygame am Anfang gemacht werden zur internen Initialisierung

# Fenstergrösse definieren
width = 700
height = 500
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Mein Erstes Pygame Programm")

black = False

if black != True:
    # Farben definieren mit RGB Wert
    white = (255, 255, 255)
    yellow = (255, 255, 0)
    red = (255, 0, 0)
    orange = (255, 100, 0)
    black = (0, 0, 0)
    green = (0, 255, 0)
    darkgreen = (0, 150, 0)
    blue = (0, 0, 255)
else:
    white = yellow = red = orange = black = green = darkgreen = blue = (0, 0, 0)

# Zeitmesser einführen
clock = pygame.time.Clock()

# Anzahl Frames
frame_count = 0

# Sonne Parameter
sonne_y = 100 # Startposition der Sonne
bewegung_y = 10 # Geschwindigkeit der Sonne
radius_sonne = 40
sonne_mittag = 100
sonne_nacht = -100


while True:
    for event in pygame.event.get():
        # If the player clicks the red 'x', it is considered a quit event
        if event.type == pygame.QUIT:
            pygame.quit() # Gegenteil von pygame.init()
            sys.exit() # Programm regulär beenden

    frame_count += 1

    # Todo: Berechne Sonnenkoordinaten
    sonne_y = ...

    # HINTERGRUND MUSS VOR DEN GEOMETRISCHEN OBJEKTEN GEZEICHNET WERDEN
    screen.fill(yellow)

    # Zeichne Sonne
    # Todo: Zeichne Sonne an der entsprechenden Koordinate
    pygame.draw.circle(screen, orange, (550, 50), radius_sonne)

    # Zeichne Grass
    # Variante 1: erstelle Rechteck-Objekt und zeichne dieses
    rechteck = pygame.Rect(0, 300, 700, 500)
    pygame.draw.rect(screen, green, rechteck)
    # Variante 2: zeichne Rechteck direkt
    # pygame.draw.rect(screen, green, (0, 300, 700, 500))

    # Zeichne Haus
    pygame.draw.rect(screen, blue, (150, 150, 300, 200))
    pygame.draw.polygon(screen, red, [(150, 150), (300, 50), (450, 150)])  # Dach
    pygame.draw.rect(screen, darkgreen, (250, 250, 50, 100))  # Türe
    pygame.draw.circle(screen, black, (260, 300), 5)  # Türgriff

    # pygame vollständig updaten
    pygame.display.update()

    clock.tick(60) # while-Schleife soll nicht öffters als 60 mal pro Sekunde ausgeführt werden.
