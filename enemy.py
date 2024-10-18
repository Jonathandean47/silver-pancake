import pygame
import random
from game_object import GameObject
from utils import create_triangle_surface

class Enemy(GameObject):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__(x, y, (50, 50), (255, 0, 0), random.choice(["up", "down", "left", "right"]), screen_width, screen_height)
        self.speed = 2
        self.original_speed = self.speed  # Store the original speed
        self.directions = ["up", "down", "left", "right"]
        self.collision_time = None  # Track the time of collision with the player
        self.last_move_time = pygame.time.get_ticks()  # Track the last move time
        self.border_offset = 15  # Shrink the border by a bit to avoid corners
        self.avoid_radius = 300  # Radius within which enemies will try to avoid the player
        self.change_direction_time = pygame.time.get_ticks()  # Track the last time direction was changed
        self.collision_cooldown = 500  # Cooldown period for direction changes after a collision (in milliseconds)
        self.health = 100  # Initial health value for the enemy
        self.max_health = 100
        self.image = create_triangle_surface(self.size, self.color, self.direction)
        self.mask = pygame.mask.from_surface(self.image)
        self.angst = random.randint(1000,5000)

    def update_size(self):
        health_ratio = self.health / self.max_health
        new_size = (max(int(50 * health_ratio), 15), max(int(50 * health_ratio), 15))
        self.image = pygame.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
    
    def change_direction(self):
        current_time = pygame.time.get_ticks()
        new_direction = random.choice(self.directions)
        while new_direction == self.direction:
            new_direction = random.choice(self.directions)
        self.direction = new_direction
        self.update_image()
        self.change_direction_time = current_time

    def update(self, player, enemies, obstacles):
        original_position = self.rect.topleft

        # Calculate distance to the player if player is not None
        if player is not None:
            distance_to_player = ((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2) ** 0.5

            if distance_to_player < self.avoid_radius:
                # Move away from the player if within the avoid radius
                if self.rect.x < player.rect.x:
                    self.rect.x -= self.speed
                    self.direction = "left"
                elif self.rect.x > player.rect.x:
                    self.rect.x += self.speed
                    self.direction = "right"
                
                if self.rect.y < player.rect.y:
                    self.rect.y -= self.speed
                    self.direction = "up"
                elif self.rect.y > player.rect.y:
                    self.rect.y += self.speed
                    self.direction = "down"

        # Random movement if outside the avoid radius or if player is None
        current_time = pygame.time.get_ticks()
        if player is None or distance_to_player >= self.avoid_radius:
            if current_time - self.change_direction_time > self.angst:  # Change direction based on self.angst
                new_direction = random.choice(self.directions)
                while new_direction == self.direction:
                    new_direction = random.choice(self.directions)
                self.direction = new_direction
                self.update_image()
                self.change_direction_time = current_time

            if self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed
            elif self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed

        # Adjust boundaries to shrink the border by a bit to avoid corners
        if self.rect.left < self.border_offset:
            self.rect.left = self.border_offset
            self.change_direction()
        if self.rect.right > self.screen_width - self.border_offset:
            self.rect.right = self.screen_width - self.border_offset
            self.change_direction()
        if self.rect.top < self.border_offset:
            self.rect.top = self.border_offset
            self.change_direction()
        if self.rect.bottom > self.screen_height - self.border_offset:
            self.rect.bottom = self.screen_height - self.border_offset
            self.change_direction()
        
        # Check for collisions with obstacles using masks and push around the object
        if len(obstacles) > 0:
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
                    self.change_direction()
                    break

        # Avoid other enemies by forcing them away by a couple of pixels when they collide
        for enemy in enemies:
            if enemy != self:
                offset = (self.rect.left - enemy.rect.left, self.rect.top - enemy.rect.top)
                collision_point = enemy.mask.overlap(self.mask, offset)
                if collision_point:
                    if self.direction == "left" or self.direction == "right":
                        if self.rect.top > enemy.rect.top:
                            self.rect.top += self.speed
                        else:
                            self.rect.top -= self.speed
                    if self.direction == "up" or self.direction == "down":
                        if self.rect.left < enemy.rect.left:
                            self.rect.left -= self.speed
                        else:
                            self.rect.left += self.speed
                    break

        # Check for collision with the player and reduce health if collided
        if player is not None:
            offset = (self.rect.left - player.rect.left, self.rect.top - player.rect.top)
            collision_point = player.mask.overlap(self.mask, offset)
            if collision_point:
                if not self.collision_time:
                    self.collision_time = pygame.time.get_ticks()
                    self.speed /= 2  # Cut speed in half on first collision
                else:
                    elapsed_time = pygame.time.get_ticks() - self.collision_time
                    if elapsed_time > 5:  # Reduce health every 5/1000 of a second of collision
                        self.health -= 5  # Reduce health by 5
                        # print(f"Enemy health reduced to {self.health}")
                        self.collision_time = pygame.time.get_ticks()  # Reset collision time

                        if self.health <= 0:  # Remove enemy if health is 0 or less
                            self.kill()
            else:
                self.collision_time = None
                # Gradually restore speed if no collision
                if self.speed < self.original_speed:
                    self.speed += 0.01  # Restore speed gradually
                if self.speed > self.original_speed:
                    self.speed = self.original_speed

        # Update size based on health
        self.update_size()
