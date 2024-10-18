import pygame
from game_object import GameObject

class CollisionSprite(GameObject):
    def __init__(self, x, y, direction, screen_width, screen_height, lifetime=500):
        super().__init__(x, y, (10, 10), (255, 255, 0), direction, screen_width, screen_height)
        self.lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Check if the sprite's lifetime has expired
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.kill()  # Remove the sprite from all groups
