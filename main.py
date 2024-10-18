import pygame
import sys
import random
from player import Player
from enemy import Enemy
from collision_sprite import CollisionSprite
from obstacle import Obstacle
from utils import create_triangle_surface, format_time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hunter")

# Load and set the window icon
icon_image = pygame.image.load(".\\assets\\icon.jpeg")
pygame.display.set_icon(icon_image)

# Custom event for spawning new enemies
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY_EVENT, 3000)  # Set timer to spawn new enemies every 3 seconds

# Font for displaying the enemy counter, win message, and timer
font = pygame.font.Font(None, 36)
timer_font = pygame.font.SysFont('courier', 24)

def spawn_enemy(enemies, obstacles, all_sprites, screen_width, screen_height):
    while True:
        x = random.randint(0, screen_width - 50)
        y = random.randint(0, screen_height - 50)
        enemy = Enemy(x, y, screen_width, screen_height)
        if not pygame.sprite.spritecollideany(enemy, obstacles):
            enemies.add(enemy)
            all_sprites.add(enemy)
            break

def run_game(player=None):
    clock = pygame.time.Clock()
    running = True

    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    if player:
        all_sprites.add(player)

    # Create some random obstacles avoiding the player's initial position if player exists
    for _ in range(10):
        while True:
            obstacle = Obstacle(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 50, 50)
            if not player or not obstacle.rect.colliderect(player.rect):
                obstacles.add(obstacle)
                all_sprites.add(obstacle)
                break

    # Ensure the player doesn't spawn in an obstacle if player exists
    if player:
        while pygame.sprite.spritecollideany(player, obstacles):
            player.rect.topleft = (random.randint(0, SCREEN_WIDTH - player.rect.width), random.randint(0, SCREEN_HEIGHT - player.rect.height))

    # Create some initial enemies
    for i in range(5):
        spawn_enemy(enemies, obstacles, all_sprites, SCREEN_WIDTH, SCREEN_HEIGHT)

    start_time = pygame.time.get_ticks()  # Record the start time

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_ENEMY_EVENT and player:
                # Spawn a new enemy at a random position avoiding obstacles
                for enemy in enemies:
                    if enemy.health > 80:
                        random_int = random.randint(0,100)
                        if random_int < (33 - len(enemies)):
                            spawn_enemy(enemies, obstacles, all_sprites, SCREEN_WIDTH, SCREEN_HEIGHT)
                    else:
                        enemy.health += 10
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Return to menu on Escape key press
                    running = False
                elif event.key == pygame.K_w and player:  # Quickly test win condition with 'W' key press
                    enemies.empty()
                elif event.key == pygame.K_e:  # Quickly test escape condition with 'E' key press
                    running = False

        if player:
            keys = pygame.key.get_pressed()
            player.update(keys, obstacles)  # Pass the obstacles group to the update method

        enemies.update(player, enemies, obstacles)  # Pass the player (or None), enemies, and obstacles group to the update method of each enemy
        collision_sprites.update()  # Update collision sprites to check their lifetime
        
        # Check for collisions using masks and obstacles for enemies
        for enemy in enemies:
            if player:
                offset = (enemy.rect.left - player.rect.left, enemy.rect.top - player.rect.top)
                collision_point = player.mask.overlap(enemy.mask, offset)
                if collision_point:
                    collision_position = (player.rect.left + collision_point[0], player.rect.top + collision_point[1])
                    # print(f"Collision detected at {collision_position} between Player and Enemy at {enemy.rect.topleft}")
                    
                    # Create a collision sprite at the collision location with the player's direction
                    collision_sprite = CollisionSprite(*collision_position, player.direction, SCREEN_WIDTH, SCREEN_HEIGHT)
                    all_sprites.add(collision_sprite)
                    collision_sprites.add(collision_sprite)

        # Check for collisions with obstacles using masks for accurate triangle interaction
        if player:
            for obstacle in obstacles:
                offset = (obstacle.rect.left - player.rect.left, obstacle.rect.top - player.rect.top)
                collision_point = player.mask.overlap(obstacle.mask, offset)
                if collision_point:
                    if player.direction == "left":
                        player.rect.x += player.speed
                    elif player.direction == "right":
                        player.rect.x -= player.speed
                    elif player.direction == "up":
                        player.rect.y += player.speed
                    elif player.direction == "down":
                        player.rect.y -= player.speed

        for enemy in enemies:
            for obstacle in obstacles:
                offset = (obstacle.rect.left - enemy.rect.left, obstacle.rect.top - enemy.rect.top)
                collision_point = enemy.mask.overlap(obstacle.mask, offset)
                if collision_point:
                    if enemy.direction == "left":
                        enemy.rect.x += enemy.speed
                    elif enemy.direction == "right":
                        enemy.rect.x -= enemy.speed
                    elif enemy.direction == "up":
                        enemy.rect.y += enemy.speed
                    elif enemy.direction == "down":
                        enemy.rect.y -= enemy.speed

        # Fill the screen with a color (RGB)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        if player:
            # Display the number of enemies on the screen
            enemy_count_text = font.render(f"Enemies: {len(enemies)}", True, (255, 255, 255))
            screen.blit(enemy_count_text, (10, 10))

            # Calculate and display the elapsed time in hh:mm:ss.fff format
            elapsed_time_ms = pygame.time.get_ticks() - start_time
            formatted_time = format_time(elapsed_time_ms)
            timer_text = timer_font.render(f"Time: {formatted_time}", True, (255, 255, 255))
            screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 10, 10))

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

def main_menu():
    menu_running = True
    clock = pygame.time.Clock()

    # Initialize background game elements
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    
    # Create some random obstacles
    for _ in range(10):
        while True:
            obstacle = Obstacle(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 50, 50)
            if not pygame.sprite.spritecollideany(obstacle, obstacles):
                obstacles.add(obstacle)
                all_sprites.add(obstacle)
                break

    # Create some initial enemies
    for i in range(5):
        spawn_enemy(enemies, obstacles, all_sprites, SCREEN_WIDTH, SCREEN_HEIGHT)

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game on Enter key press
                    run_game(Player(SCREEN_WIDTH, SCREEN_HEIGHT))
                elif event.key == pygame.K_ESCAPE:  # Quit game on Escape key press
                    menu_running = False

        # Run the background game loop without a player and without spawning events
        enemies.update(None, enemies, obstacles)  # Pass None for player since there's no player in the background game
        collision_sprites.update()  # Update collision sprites to check their lifetime
        
        # Fill the screen with a color (RGB)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        # Display menu text over the background game loop
        title_text = font.render("HUNTER", True, (255, 255, 255))
        start_text = font.render("Press Enter to Start", True, (255, 255, 255))
        quit_text = font.render("Press Escape to Quit", True, (255, 255, 255))

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 40))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 - quit_text.get_height() // 2 + 40))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
    pygame.quit()
    sys.exit()
