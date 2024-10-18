import pygame
from game_object import GameObject
from utils import create_triangle_surface

class Player(GameObject):
    def __init__(self, screen_width, screen_height):
        self.x = screen_width // 2
        self.y = screen_height // 2
        super().__init__(self.x, self.y, (50, 50), (0, 128, 255), "up", screen_width, screen_height)
        self.speed = 5
        self.image = create_triangle_surface(self.size, self.color, self.direction)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, keys, obstacles):
        original_position = self.rect.topleft

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

        # Check for collisions with obstacles using masks
        for obstacle in obstacles:
            offset = (obstacle.rect.left - self.rect.left, obstacle.rect.top - self.rect.top)
            collision_point = self.mask.overlap(obstacle.mask, offset)
            if collision_point:
                if self.rect.right > obstacle.rect.right:
                    # push us back the way we're coming from
                    self.rect.x += self.speed
                    # if the tip of the entity is above the obstacle push it up
                    if ((self.rect.top + self.rect.bottom)/2) > obstacle.rect.top:
                        self.rect.y += self.speed
                    # if the tip of the entitiy is below the obstacle push it down
                    elif ((self.rect.top + self.rect.bottom)/2) < obstacle.rect.bottom:
                        self.rect.y -= self.speed
                if self.rect.left < obstacle.rect.left:
                    # push us back the way we're coming from
                    self.rect.x -= self.speed
                    # if the tip of the entity is above the obstacle push it up
                    if ((self.rect.top + self.rect.bottom)/2) > obstacle.rect.top:
                        self.rect.y += self.speed
                    # if the tip of the entitiy is below the obstacle push it down
                    elif ((self.rect.top + self.rect.bottom)/2) < obstacle.rect.bottom:
                        self.rect.y -= self.speed
                if self.rect.bottom > obstacle.rect.bottom:
                    self.rect.y += self.speed
                    if ((self.rect.left + self.rect.right)/2) < obstacle.rect.left:
                        self.rect.x -= self.speed
                    elif ((self.rect.left + self.rect.right)/2) > obstacle.rect.right:
                        self.rect.x += self.speed
                if self.rect.top < obstacle.rect.top:
                    self.rect.y -= self.speed
                    if ((self.rect.left + self.rect.right)/2) < obstacle.rect.left:
                        self.rect.x -= self.speed
                    elif ((self.rect.left + self.rect.right)/2) > obstacle.rect.right:
                        self.rect.x += self.speed
                break

        self.check_boundaries()
