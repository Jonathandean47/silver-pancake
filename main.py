import pygame
import sys
import random
from player import Player
from enemy import Enemy
from collision_sprite import CollisionSprite
from obstacle import Obstacle
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
pygame.time.set_timer(SPAWN_ENEMY_EVENT, 3000)  # Set timer to spawn new enemies every 3 seconds

# Font for displaying the enemy counter and win message
font = pygame.font.Font(None, 36)

def spawn_enemy(enemies, obstacles, all_sprites, screen_width, screen_height):
    while True:
        x = random.randint(0, screen_width - 50)
        y = random.randint(0, screen_height - 50)
        enemy = Enemy(x, y, screen_width, screen_height)
        if not pygame.sprite.spritecollideany(enemy, obstacles):
            enemies.add(enemy)
            all_sprites.add(enemy)
            break

def main_game():
    clock = pygame.time.Clock()
    running = True

    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    all_sprites.add(player)
    
    # Create some random obstacles avoiding the player's initial position
    for _ in range(10):
        while True:
            obstacle = Obstacle(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 50, 50)
            if not obstacle.rect.colliderect(player.rect):
                obstacles.add(obstacle)
                all_sprites.add(obstacle)
                break

    # Ensure the player doesn't spawn in an obstacle
    while pygame.sprite.spritecollideany(player, obstacles):
        player.rect.topleft = (random.randint(0, SCREEN_WIDTH - player.rect.width), random.randint(0, SCREEN_HEIGHT - player.rect.height))

    # Create some initial enemies
    for i in range(5):
        spawn_enemy(enemies, obstacles, all_sprites, SCREEN_WIDTH, SCREEN_HEIGHT)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_ENEMY_EVENT:
                # Spawn a new enemy at a random position avoiding obstacles
                spawn_enemy(enemies, obstacles, all_sprites, SCREEN_WIDTH, SCREEN_HEIGHT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Return to menu on Escape key press
                    running = False

        keys = pygame.key.get_pressed()
        player.update(keys, obstacles)  # Pass the obstacles group to the update method
        enemies.update(player, enemies, obstacles)  # Pass the player, enemies, and obstacles group to the update method of each enemy
        collision_sprites.update()  # Update collision sprites to check their lifetime
        
        # Check for collisions using masks and obstacles for enemies
        for enemy in enemies:
            offset = (enemy.rect.left - player.rect.left, enemy.rect.top - player.rect.top)
            collision_point = player.mask.overlap(enemy.mask, offset)
            if collision_point:
                collision_position = (player.rect.left + collision_point[0], player.rect.top + collision_point[1])
                # print(f"Collision detected at {collision_position} between Player and Enemy at {enemy.rect.topleft}")
                
                # Create a collision sprite at the collision location with the player's direction
                collision_sprite = CollisionSprite(*collision_position, player.direction, SCREEN_WIDTH, SCREEN_HEIGHT)
                all_sprites.add(collision_sprite)
                collision_sprites.add(collision_sprite)

        # Fill the screen with a color (RGB)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        # Display the number of enemies on the screen
        enemy_count_text = font.render(f"Enemies: {len(enemies)}", True, (255, 255, 255))
        screen.blit(enemy_count_text, (10, 10))

        # Check for win condition (no enemies left)
        if len(enemies) == 0:
            win_text = font.render("You Win!", True, (255, 255, 255))
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)  # Display win message for 3 seconds
            running = False

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    main_menu()  # Return to main menu after game ends

def main_menu():
    menu_running = True

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game on Enter key press
                    main_game()
                elif event.key == pygame.K_ESCAPE:  # Quit game on Escape key press
                    menu_running = False

        screen.fill((0, 0, 0))

        title_text = font.render("RPG Game", True, (255, 255, 255))
        start_text = font.render("Press Enter to Start", True, (255, 255, 255))
        quit_text = font.render("Press Escape to Quit", True, (255, 255, 255))

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 40))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 - quit_text.get_height() // 2 + 40))

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
    pygame.quit()
    sys.exit()
