from typing import List, Tuple
import pygame
import config
from math import sqrt, ceil
from random import randint


class Map:
    def __init__(self, file_path: str, player_count: int = 4):
        # Save path and player count
        self.file_path = file_path
        self.player_count = player_count
        # Load map from file
        self.inner_map: List[List[str]] = self.get_map()

    def tile_to_pixel(self, x: int, y: int) -> Tuple[int, int]:
        """Convert tile (col, row) to pixel (x, y)"""
        px = (x + 1) * config.TILE_SIZE + config.TILE_SIZE // 2
        py = (y + 1) * config.TILE_SIZE + config.TILE_SIZE // 2
        return (px, py)

    def generate_spawn_positions(self) -> List[Tuple[int, int]]:
        """Generate spaced-out spawn positions (pixels) avoiding invalid tiles."""
        spawn_positions: List[Tuple[int, int]] = []
        spawn_tiles: List[Tuple[int, int]] = []

        rows = len(self.inner_map)
        cols = len(self.inner_map[0])

        min_col_dist = ceil(cols / self.player_count)
        min_row_dist = ceil(rows / self.player_count)
        min_euclidean_dist = sqrt(min_col_dist ** 2 + min_row_dist ** 2)

        attempts = 0
        while len(spawn_tiles) < self.player_count:
            col = randint(2, cols - 3)
            row = randint(2, rows - 3)
            attempts += 1

            if self.inner_map[row][col] in ("wall", "lava", "bush"):
                continue

            too_close = False
            for (c, r) in spawn_tiles:
                dist = sqrt((col - c) ** 2 + (row - r) ** 2)
                if dist < min_euclidean_dist:
                    too_close = True
                    break

            if not too_close:
                spawn_tiles.append((col, row))
                px, py = self.tile_to_pixel(col, row)
                spawn_positions.append((px, py))
                print(f"[INFO] Player {len(spawn_tiles) - 1} -> tile ({col}, {row}) -> pixel ({px}, {py})")

        print(f"Found {self.player_count} spawnpoints in {attempts} attempts.")
        return spawn_positions

    def walls(self) -> List[pygame.Rect]:
        """Return all wall tiles as pygame.Rects for collision checks."""
        wall_rects = []
        for y in range(len(self.inner_map)):
            for x in range(len(self.inner_map[0])):
                if self.inner_map[y][x] == "wall":
                    rect = pygame.Rect(
                        x * config.TILE_SIZE,
                        y * config.TILE_SIZE,
                        config.TILE_SIZE,
                        config.TILE_SIZE,
                    )
                    wall_rects.append(rect)
        return wall_rects

    def wall_tiles(self) -> List[Tuple[int, int]]:
        """Return all wall tile positions as (x, y) tile coordinates."""
        return [
            (x, y)
            for y in range(len(self.inner_map))
            for x in range(len(self.inner_map[0]))
            if self.inner_map[y][x] == "wall"
        ]

    def get_tile_type(self, x: int, y: int) -> str:
        """Return the tile type at (x, y) if it's inside the map."""
        rows = len(self.inner_map)
        cols = len(self.inner_map[0])
        if 0 <= y < rows and 0 <= x < cols:
            return self.inner_map[y][x]

    def get_map(self) -> List[List[str]]:
        """Read the map file and convert characters to tile types."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if len(lines) != config.ROWS - 2:
            raise ValueError(f"The file must have exactly {config.ROWS - 2} rows.")

        map_data: List[List[str]] = []
        for line in lines:
            line = line.rstrip("\n")
            if len(line) != config.COLUMNS - 2:
                raise ValueError(
                    f"Each line must have exactly {config.COLUMNS - 2} columns."
                )

            row = []
            for char in line:
                row.append(
                    {
                        "g": "ground",
                        "w": "wall",
                        "l": "lava",
                        "i": "ice",
                        "s": "sand",
                        "b": "bush",
                    }.get(char, "ground")
                )  # fallback if invalid character

            map_data.append(row)

        return map_data
