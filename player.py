import pygame
from game_object import GameObject

class Player(GameObject):
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width // 2, screen_height // 2, (50, 50), (0, 128, 255), "down", screen_width, screen_height)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "right"
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = "up"
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = "down"
        
        self.check_boundaries()
        self.update_image()
