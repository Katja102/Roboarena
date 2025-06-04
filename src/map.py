from typing import List, Tuple
import pygame
import config
from math import sqrt, ceil
from random import randint
from fallback_map import get_fallback_map

class Map:
    def __init__(self, file_path: str | None = None, player_count: int = 4):
        """Initializes the map with default player-size and optional file input"""
        self.player_count = player_count
        self.file_path = file_path
        self.rows = config.ROWS
        self.cols = config.COLUMNS

        # Initialize map with a basic layout (outer walls, ground inside)
        self.map_data = self.initialize_map()

        # If a file path is provided: load from file, otherwise use the fallback map
        try:
            inner_map = self.get_inner_map()
        except FileNotFoundError:
            print(f"[Warning] File '{self.file_path}' not found. Using fallback map.")
            inner_map = get_fallback_map()

        self.create_map(inner_map)

    def initialize_map(self) -> list[list[str]]:
        """Creates an empty map with walls around and ground inside"""
        map_data = []
        for y in range(self.rows):
            row = []
            for x in range(self.cols):
                is_border = x == 0 or x == self.cols - 1 or y == 0 or y == self.rows - 1
                tile = "wall" if is_border else "ground"
                row.append(tile)
            map_data.append(row)
        return map_data

    def get_inner_map(self) -> List[List[str]]:
        """Read map file and convert characters to tile types"""
        with open(self.file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if len(lines) != self.rows - 2:
            raise ValueError(f"The file must have exactly {self.rows - 2} rows.")

        char_to_tile = {
            "g": "ground",
            "w": "wall",
            "l": "lava",
            "i": "ice",
            "s": "sand",
            "b": "bush",
        }

        map_data: List[List[str]] = []
        for line in lines:
            line = line.rstrip("\n")
            if len(line) != self.cols - 2:
                raise ValueError(
                    f"Each line must have exactly {self.cols - 2} columns."
                )

            row = []
            for char in line:
                if char in char_to_tile:
                    row.append(char_to_tile[char])
                else:
                    row.append("ground")  # fill with ground if invalid char
            map_data.append(row)

        return map_data

    def create_map(self, inner_map: list[list[str]]) -> None:
        """
        Fill the central part of self.map_data with the given inner_map
        """
        for y in range(len(inner_map)):
            for x in range(len(inner_map[0])):
                self.map_data[y + 1][x + 1] = inner_map[y][x]
                # fill map_data with inner_map (offset by one)

    def tile_to_pixel(self, x: int, y: int) -> Tuple[int, int]:
        """Convert tile (col, row) to pixel (x, y)
        (Used in generate_spawn_positions)"""
        px = x * config.TILE_SIZE + config.TILE_SIZE // 2
        py = y * config.TILE_SIZE + config.TILE_SIZE // 2
        return (px, py)

    def generate_spawn_positions(self) -> List[Tuple[int, int]]:
        """Generate spawn positions (pixels) avoiding invalid tiles"""
        spawn_positions: List[Tuple[int, int]] = []
        spawn_tiles: List[Tuple[int, int]] = []

        min_col_dist = ceil(self.cols / self.player_count)
        min_row_dist = ceil(self.rows / self.player_count)
        min_euclidean_dist = sqrt(min_col_dist**2 + min_row_dist**2)

        while len(spawn_tiles) < self.player_count:
            col = randint(2, self.cols - 3)
            row = randint(2, self.rows - 3)

            if self.map_data[row][col] in ("wall", "lava", "bush"):
                continue

            too_close = False
            for (
                c,
                r,
            ) in (
                spawn_tiles
            ):  # Skip distance check for Player 0 (no previous spawns yet)
                dist = sqrt((col - c) ** 2 + (row - r) ** 2)
                if dist < min_euclidean_dist:
                    too_close = True
                    break

            if not too_close:
                spawn_tiles.append((col, row))
                px, py = self.tile_to_pixel(col, row)
                spawn_positions.append((px, py))

        return spawn_positions

    def walls(self) -> List[pygame.Rect]:
        """Return all wall tiles as pygame.Rects for collision check"""
        wall_rects = []
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[0])):
                if self.map_data[y][x] == "wall":
                    rect = pygame.Rect(
                        x * config.TILE_SIZE,
                        y * config.TILE_SIZE,
                        config.TILE_SIZE,
                        config.TILE_SIZE,
                    )
                    wall_rects.append(rect)
        return wall_rects

    def get_tile_type(self, x: int, y: int) -> str | None:
        """Return the tile type at (x, y)"""
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return self.map_data[y][x]
        return "void"

    def get_map_data(self):
        """Return map data"""
        return self.map_data
