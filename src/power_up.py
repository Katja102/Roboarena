import pygame
import config
import random
from map import Map
from camera import Camera

# Constants
size: int = 30


class Powerup:
    def __init__(self, powerup_type: str, game_map: Map):
        self.rect = self.spawn_pos(game_map)
        self.type = powerup_type
        self.alive = True  # if bullet is there

    def draw_powerup(self, camera: Camera) -> None:
        # draw powerup
        draw_x, draw_y = camera.apply(int(self.rect.x), int(self.rect.y))
        if self.type == "double_speed":
            pygame.draw.circle(camera.surface, (250, 0, 0), (draw_x, draw_y), 3)
        if self.type == "health_boost":
            pygame.draw.circle(camera.surface, (0, 250, 0), (draw_x, draw_y), 3)
        if self.type == "power_boost":
            pygame.draw.circle(camera.surface, (0, 0, 250), (draw_x, draw_y), 3)
        if self.type == "indestructible":
            pygame.draw.circle(camera.surface, (0, 0, 250), (draw_x, draw_y), 3)

    # Get the list of tiles touched by the robot
    def touched_tiles(self) -> list[tuple[int, int]]:

        x_bounds = [
            self.rect.left // config.TILE_SIZE,
            (self.rect.right - 1) // config.TILE_SIZE,
        ]
        y_bounds = [
            self.rect.top // config.TILE_SIZE,
            (self.rect.bottom - 1) // config.TILE_SIZE,
        ]
        touching_tiles = []
        for i in range(x_bounds[0], x_bounds[1] + 1):
            for j in range(y_bounds[0], y_bounds[1] + 1):
                touching_tiles.append((i, j))
        return touching_tiles

    # Get the textures of the tiles touched by the robot
    def touched_textures(self, game_map: Map) -> set[str]:
        touched_textures = set()
        for [i, j] in self.touched_tiles():
            touched_textures.add(game_map.get_tile_type(i, j))
        return touched_textures

    def spawn_pos(self, game_map: Map) -> pygame.Rect:
        # Get random position
        position_x = random.randint(
            2 * config.TILE_SIZE,
            (config.COLUMNS - 2) * config.TILE_SIZE,
        )
        position_y = random.randint(
            2 * config.TILE_SIZE,
            (config.ROWS - 2) * config.TILE_SIZE,
        )
        self.rect = pygame.Rect(position_x, position_y, size, size)
        # Check for tiles to avoid walls, lava and bush
        touched_textures = self.touched_textures(game_map)
        if (
            ("lava" not in touched_textures)
            and ("wall" not in touched_textures)
            and ("bush" not in touched_textures)
        ):
            return self.rect
        return self.spawn_pos(game_map)
