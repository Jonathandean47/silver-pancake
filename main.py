import pygame
import sys
import random
from player import Player
from enemy import Enemy
from collision_sprite import CollisionSprite
from utils import create_triangle_surface

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple RPG Game")

# Custom event for spawning new enemies
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY_EVENT, 2000)  # Set timer to spawn new enemies every 2 seconds

def main():
    clock = pygame.time.Clock()
    running = True

    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    # Create some initial enemies
    for i in range(5):
        enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT)
        enemies.add(enemy)
        all_sprites.add(enemy)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_ENEMY_EVENT:
                # Spawn a new enemy at a random position
                enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(enemy)
                all_sprites.add(enemy)

        keys = pygame.key.get_pressed()
        player.update(keys)
        enemies.update(player, enemies)  # Pass the player and enemies group to the update method of each enemy
        collision_sprites.update()  # Update collision sprites to check their lifetime
        
        # Check for collisions using masks
        for enemy in enemies:
            offset = (enemy.rect.left - player.rect.left, enemy.rect.top - player.rect.top)
            collision_point = player.mask.overlap(enemy.mask, offset)
            if collision_point:
                collision_position = (player.rect.left + collision_point[0], player.rect.top + collision_point[1])
                print(f"Collision detected at {collision_position} between Player and Enemy at {enemy.rect.topleft}")
                
                # Create a collision sprite at the collision location with the player's direction
                collision_sprite = CollisionSprite(*collision_position, player.direction, SCREEN_WIDTH, SCREEN_HEIGHT)
                all_sprites.add(collision_sprite)
                collision_sprites.add(collision_sprite)

        # Fill the screen with a color (RGB)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
