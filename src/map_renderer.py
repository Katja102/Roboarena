import pygame
import config


class MapRenderer:
    def __init__(self, screen: pygame.Surface, textures: dict[str, pygame.Surface]):
        """Draws the map on the screen."""
        self.screen = screen                         # current game screen
        self.textures = textures                     # tile type to texture mapping
        self.map_picture = None                      # rendered map surface

    def draw_map_picture(self, map_data: list[list[str]]) -> None:
        """Creates the map image (not shown yet)."""
        rows = len(map_data)
        cols = len(map_data[0])
        height = rows * config.TILE_SIZE
        width = cols * config.TILE_SIZE
        self.map_picture = pygame.Surface((width, height))

        for y in range(rows):
            for x in range(cols):
                tile_type = map_data[y][x]
                texture = self.textures[tile_type].convert()
                texture = pygame.transform.scale(texture, (config.TILE_SIZE, config.TILE_SIZE))
                self.map_picture.blit(texture, (x * config.TILE_SIZE, y * config.TILE_SIZE))

    def draw_map(self) -> None:
        """Shows the map image on the screen."""
        if self.map_picture:
            self.screen.blit(self.map_picture, (0, 0))
