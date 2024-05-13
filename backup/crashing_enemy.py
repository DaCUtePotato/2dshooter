import pygame
class crashingEnemy:
    def __init__(self, x, y, width, height, hp, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.speed = speed
        self.rect = pygame.Rect(x, y, width, height)  # Initialize rect attribute

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y
