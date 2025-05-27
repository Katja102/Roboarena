import pygame
import sys
import config
import map
from arena import Arena
from robot import Robot

# Initialisation
pygame.init()

# Get current screen resolution
info = pygame.display.Info()
max_width: int = info.current_w
max_height: int = info.current_h

# Calculate TILE_SIZE to fit the fixed grid into the screen
config.TILE_SIZE = min(max_width // config.COLUMNS, max_height // config.ROWS)

# set window size
window_width: int = config.TILE_SIZE * config.COLUMNS
window_height: int = config.TILE_SIZE * config.ROWS

# Create window (not fullscreen)
screen: pygame.Surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Roboarena")
clock = pygame.time.Clock()

# Debug info
print(f"Monitor: {max_width}x{max_height}")
print(f"Fenster: {window_width}x{window_height}")
print(f"TILE_SIZE: {config.TILE_SIZE}")

# Load map and arena
arena: Arena = Arena(screen, config.ROWS, config.COLUMNS, config.TEXTURES)
arena.create_map(map.get_map("test-level.txt"))

player: Robot = Robot(screen, 500, 500, 20, 180, (255, 255, 255), 1, 1)
enemy1: Robot = Robot(screen, 800, 300, 30, 0, (0, 100, 190), 1, 1)
enemy2: Robot = Robot(screen, 300, 600, 40, 50, (255, 50, 120), 1, 1)
enemy3: Robot = Robot(screen, 1200, 600, 40, 50, (0, 250, 0), 1, 1)

robots: list[Robot] = [player, enemy1, enemy2, enemy3]

circle_tick: int = 50
angle: int = 180


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

    screen.fill((220, 220, 220))  # light gray background
    arena.draw_map()
    ticks = pygame.time.get_ticks()
    player.update_player(robots)
    if ticks > circle_tick:
        circle_tick += 50
        angle = (angle + 3) % 360
    enemy1.move_circle((800, 300), 50, angle, robots)
    enemy2.update_enemy(player, robots)
    enemy3.update_enemy(player, robots)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
