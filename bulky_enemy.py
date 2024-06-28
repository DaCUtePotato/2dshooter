import random

# Bulky attributes
class Bulky:
    def __init__(self, x, y, width, height, hp, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.speed = speed
        self.frame = 0
        self.frame_count = 0
        self.death_animation_playing = False
        self.death_frame = 0
        self.death_frame_count = 0

exp = random.randint(10, 50)
bulkies = []
