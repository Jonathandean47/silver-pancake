import pygame
import random
from utils import create_triangle_surface

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__()
        self.size = (50, 50)
        self.color = (255, 0, 0)
        self.directions = ["up", "down", "left", "right"]
        self.direction = random.choice(self.directions)
        self.image = create_triangle_surface(self.size, self.color, self.direction)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        
        # Change direction randomly
        if random.randint(1, 100) > 98:  # 2% chance to change direction
            self.direction = random.choice(self.directions)
            self.image = create_triangle_surface(self.size, self.color, self.direction)
            self.mask = pygame.mask.from_surface(self.image)
