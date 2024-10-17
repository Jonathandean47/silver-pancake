import pygame
from utils import create_triangle_surface

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, lifetime=500):
        super().__init__()
        self.size = (50, 50)
        self.color = (255, 255, 0)  # Yellow color for collision
        self.image = create_triangle_surface(self.size, self.color, "up")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Check if the sprite's lifetime has expired
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.kill()  # Remove the sprite from all groups
