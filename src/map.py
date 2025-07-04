from typing import List, Tuple
import pygame
import config
from pathlib import Path
from math import sqrt, ceil
from random import randint
from fallback_map import get_fallback_map


class Map:
    def __init__(self, file_path: str | None = None, player_count: int = 4, random_map: bool = False):
        """Initializes the map with default player-size and optional file input"""
        self.player_count = player_count
        self.file_path = file_path
        self.random_map = random_map
        self.rows = config.ROWS
        self.cols = config.COLUMNS

        # Initialize map with a basic layout (outer walls, ground inside)
        self.map_data = self.initialize_map()

        # If a file path is provided: load from file, otherwise use the fallback map

        if random_map:
            inner_map = self.generate_random_inner_map()
        elif self.file_path is not None:
            try:
                inner_map = self.get_inner_map()
            except FileNotFoundError:
                print(f"Warning: file {self.file_path} not found. Using fallback map.")
                inner_map = get_fallback_map()
        else:

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


    def generate_random_inner_map(self) -> list[list[str]]:
        inner_map = []
        for y in range(self.rows - 2):  # ohne Rahmen
            row = ["ground"] * (self.cols - 2)
            inner_map.append(row)

        # create patches (this can be adjusted manually)
        self.generate_patch(inner_map, tile="wall", num_patches=5, min_size=2, max_size=15)
        self.generate_patch(inner_map, tile="bush", num_patches=6, min_size=1, max_size=5)
        self.generate_patch(inner_map, tile="lava", num_patches=4, min_size=1, max_size=9)
        self.generate_patch(inner_map, tile="sand", num_patches=5, min_size=3, max_size=7)
        self.generate_patch(inner_map, tile="ice", num_patches=7, min_size=1, max_size=5)

        return inner_map

    def generate_patch(
            self,
            map_data: list[list[str]],
            tile: str,
            num_patches: int,
            min_size: int,
            max_size: int,
            irregular: bool = True
    ) -> None:
        for _ in range(num_patches):
            width = randint(min_size, max_size)
            height = randint(min_size, max_size)
            start_x = randint(1, self.cols - 2 - width - 1)
            start_y = randint(1, self.rows - 2 - height - 1)

            if irregular:
                init_start_x = randint(3, self.cols - 2 - max_size)

            for i in range(height):
                if irregular:
                    width = randint(int(0.7 * max_size), max_size)
                    start_x = init_start_x - randint(1, 2)
                for j in range(width):
                    map_data[start_y + i][start_x + j] = tile



    def get_inner_map(self) -> List[List[str]] | None:

        """Read map file and convert characters to tile types"""
        if not self.file_path:
            return None
        with open(Path(self.file_path), "r", encoding="utf-8") as file:
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
