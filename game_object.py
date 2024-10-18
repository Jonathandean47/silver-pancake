import pygame
from utils import create_triangle_surface

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, direction, screen_width, screen_height):
        super().__init__()
        self.size = size
        self.color = color
        self.direction = direction
        self.image = create_triangle_surface(self.size, self.color, self.direction)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mask = pygame.mask.from_surface(self.image)

    def update_image(self):
        self.image = create_triangle_surface(self.size, self.color, self.direction)
        self.mask = pygame.mask.from_surface(self.image)

    def check_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
