import pygame
import config
from camera import Camera


class MapRenderer:
    def __init__(
        self, camera_surface: pygame.Surface, textures: dict[str, pygame.Surface]
    ):
        """Draws the map on the screen."""
        self.camera_surface = camera_surface  # current visible screen
        self.textures = textures  # tile type to texture mapping
        self.map_picture = None  # rendered map surface

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
                texture = pygame.transform.scale(
                    texture, (config.TILE_SIZE, config.TILE_SIZE)
                )
                self.map_picture.blit(
                    texture, (x * config.TILE_SIZE, y * config.TILE_SIZE)
                )

    def draw_map(self, camera: Camera) -> None:
        """Shows the visible part of the map through the camera."""
        if self.map_picture:
            # Move map based on camera offset and scale
            offset_x = int(-camera.offset_x * camera.zoom)
            offset_y = int(-camera.offset_y * camera.zoom)

            # Scale map according to zoom level
            scaled_map = pygame.transform.scale(
                self.map_picture,
                (
                    int(self.map_picture.get_width() * camera.zoom),
                    int(self.map_picture.get_height() * camera.zoom),
                ),
            )
            # Draw the zoomed map
            self.camera_surface.blit(scaled_map, (offset_x, offset_y))
