import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, shape=random.choice(["rectangle","circle","triangle"])):
        super().__init__()
        self.shape = shape
        print(f"{self.shape}")
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Allow transparency
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Draw the shape
        if self.shape == 'rectangle':
            pygame.draw.rect(self.image, (128, 128, 128), self.image.get_rect())
        elif self.shape == 'circle':
            pygame.draw.circle(self.image, (128, 128, 128), (width // 2, height // 2), min(width, height) // 2)
        elif self.shape == 'triangle':
            pygame.draw.polygon(self.image, (128, 128, 128), [(0, height), (width // 2, 0), (width, height)])
            
        self.mask = pygame.mask.from_surface(self.image)
