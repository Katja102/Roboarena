import pygame


# Global constants

# Tile textures by type
TEXTURES: dict[str, pygame.Surface] = {
    "ground": pygame.image.load("../resources/Textures/Floor.png"),  # ground
    "wall": pygame.image.load("../resources/Textures/Wall.png"),  # walls
    "lava": pygame.image.load("../resources/Textures/Lava.png"),  # lava
    "ice": pygame.image.load("../resources/Textures/Ice.png"),  # ice
    "sand": pygame.image.load("../resources/Textures/Sand.png"),  # sand
    "bush": pygame.image.load("../resources/Textures/Bush.png"),  # bush
}

# Icon textures for UI
ICONS: dict[str, pygame.Surface] = {
    "heart": pygame.image.load("../resources/Icons/Heart.png"),  # HP icon
    "power": pygame.image.load("../resources/Icons/Power.png"),  # Power icon
}


TILE_SIZE: int = 0  # will be assigned during runtime in main.py
COLUMNS: int = 48  # number of tile columns (horizontal)
ROWS: int = 27  # number of tile rows (vertical)
ZOOM: float = 1.3  # scaling factor applied to all tiles and objects
ROBOT_RENDER_SIZE = 64 # always 64x64 px
SHOW_STATS: bool = True # Toggle to show or hide HP and Power numbers


