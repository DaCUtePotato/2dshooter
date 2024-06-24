# base_enemy.py
import pygame

class Enemy:
    def __init__(self, x, y, width, height, hp, speed, frame):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.speed = speed
        self.frame = frame

# Keep track of all enemies
enemies = []
