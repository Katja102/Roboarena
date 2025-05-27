import pygame
import config


class Arena:
    def __init__(
        self,
        screen: pygame.Surface,
        rows: int,
        columns: int,
        textures: dict[str, pygame.Surface]
    ):
        self.screen = screen  # current game screen
        self.rows = rows  # number of rows
        self.columns = columns  # number of columns
        self.textures = textures  # possible tile textures
        self.grid = self.initialise_map()  # fill grid with floor and outer walls
        self.map_picture = None  # complete map for the arena, to render it only once

    def initialise_map(self) -> list[list[str]]:
        grid = []
        for r in range(self.rows):
            current_row = []
            for c in range(self.columns):
                if c == 0 or r == 0 or r == self.rows - 1 or c == self.columns - 1:
                    current_row.append("wall")  # outer edges
                else:
                    current_row.append("ground")  # inner tiles
            grid.append(current_row)
        return grid

    def create_map(self, map_data: list) -> None:
        expected_rows = self.rows - 2
        expected_columns = self.columns - 2
        for row in map_data:  # check if map_data is in invalid format
            if len(map_data) != expected_rows:
                raise ValueError(
                    f"Map must have exactly {expected_rows}"
                    f" rows but got {len(map_data)}."
                )
            if len(row) != expected_columns:
                raise ValueError(
                    f"Map must have exactly {expected_columns}"
                    f" rows but got {len(row)}."
                )
        for r in range(expected_rows):
            for c in range(expected_columns):
                self.grid[r + 1][c + 1] = map_data[r][
                    c
                ]  # assign inner tiles of current
                # map to map_data with format-Offset 1
        self.draw_map_picture()

    def draw_map_picture(self) -> None:
        width = self.columns * config.TILE_SIZE
        height = self.rows * config.TILE_SIZE
        self.map_picture = pygame.Surface((width, height))
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * config.TILE_SIZE
                y = row * config.TILE_SIZE
                tile_type = self.grid[row][col]
                texture = self.textures[tile_type].convert()
                texture = pygame.transform.scale(
                    texture, (config.TILE_SIZE, config.TILE_SIZE)
                )
                self.map_picture.blit(texture, (x, y))

    def draw_map(self) -> None:
        if self.map_picture:
            self.screen.blit(self.map_picture, (0, 0))
