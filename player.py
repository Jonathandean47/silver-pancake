import pygame
from utils import create_triangle_surface

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.size = (50, 50)
        self.color = (0, 128, 255)
        self.direction = "down"
        self.image = create_triangle_surface(self.size, self.color, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)

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
        
        self.image = create_triangle_surface(self.size, self.color, self.direction)
        self.mask = pygame.mask.from_surface(self.image)
