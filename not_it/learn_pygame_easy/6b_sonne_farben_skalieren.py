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
red = (255, 0, 0)
orange = (255, 100, 0)
black = (0, 0, 0)
green = (0, 255, 0)
darkgreen = (0, 150, 0)
blue = (0, 0, 255)

# Zeitmesser einführen
clock = pygame.time.Clock()

# Anzahl Frames
frame_count = 0

# Sonne Koordinaten
sonne_y = 50
bewegung_y = 2
radius_sonne = 40
sonne_max = 50 # maximale Höhe
sonne_min = 300 # minimale Höhe

def farbe_skaliert(höhe, höhe_min, höhe_max, farbe1, farbe2 = (0,0,0)):
    skalierte_farbe = []
    for i in range(3): # Iteration über die drei Farbkanäle
        # Todo: berechne den Farbwert neu anhand der Höhe der Sonne
        neuer_farbwert = farbe1[i] # diese Zeile muss ersetzt werden

        if neuer_farbwert > 255: # Sollte der Farbwert leicht überschritten werden, so setze diesen auf 255
            skalierte_farbe.append(255)
        elif neuer_farbwert < 0: # Wir wollen keine negativen Farbwerte
            skalierte_farbe.append(0)
        else:
            skalierte_farbe.append(neuer_farbwert)
    return skalierte_farbe


while True:
    for event in pygame.event.get():
        # If the player clicks the red 'x', it is considered a quit event
        if event.type == pygame.QUIT:
            pygame.quit() # Gegenteil von pygame.init()
            sys.exit() # Programm regulär beenden

    frame_count += 1

    # Berechne Sonnenkoordinaten
    sonne_y = sonne_y + bewegung_y
    if sonne_y > sonne_min + radius_sonne and bewegung_y > 0:
        bewegung_y = -bewegung_y
    elif sonne_y < sonne_max and bewegung_y < 0:
        bewegung_y = -bewegung_y

    # HINTERGRUND MUSS VOR DEN GEOMETRISCHEN OBJEKTEN GEZEICHNET WERDEN
    # Todo: ersetze Farbe mit skalierter Farbe: farbe_skaliert(???, ???, ???, (100, 100, 255))
    screen.fill((100, 100, 255))

    # Zeichne Sonne
    pygame.draw.circle(screen, orange, (550, sonne_y), radius_sonne)

    # Zeichne Grass
    rechteck = pygame.Rect(0, 300, 700, 500)
    # Todo: ersetze Farbe mit skalierter Farbe: farbe_skaliert(???, ???, ???, green)
    pygame.draw.rect(screen, green, rechteck)


    # Zeichne Haus
    # Todo: ersetze alle Farben mit skalierter Farbe
    pygame.draw.rect(screen, farbe_skaliert(sonne_y, sonne_max, sonne_min, blue), (150, 150, 300, 200))
    pygame.draw.polygon(screen, farbe_skaliert(sonne_y, sonne_max, sonne_min, red), [(150, 150), (300, 50), (450, 150)])  # Dach
    pygame.draw.rect(screen, farbe_skaliert(sonne_y, sonne_max, sonne_min, darkgreen), (250, 250, 50, 100))  # Türe
    pygame.draw.circle(screen, black, (260, 300), 5)  # Türgriff

    # pygame vollständig updaten
    pygame.display.update()

    clock.tick(60) # while-Schleife soll nicht öffters als 60 mal pro Sekunde ausgeführt werden.
