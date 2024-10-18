import pygame
import random
from game_object import GameObject

class Enemy(GameObject):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__(x, y, (50, 50), (255, 0, 0), random.choice(["up", "down", "left", "right"]), screen_width, screen_height)
        self.speed = 2
        self.directions = ["up", "down", "left", "right"]

    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        
        self.check_boundaries()
        
        # Change direction randomly
        if random.randint(1, 100) > 98:  # 2% chance to change direction
            self.direction = random.choice(self.directions)
            self.update_image()
