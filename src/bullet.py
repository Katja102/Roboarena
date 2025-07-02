import pygame
import math
import config
from map import Map
from camera import Camera


class Bullet:
    def __init__(
        self,
        x: int,
        y: int,
        direction: float,
        radius: int,
        color: tuple[int, int, int],
        shooter,  # :Robot
        velocity: float,
        reach: int,
    ):
        self.x = x  # x-coordiante of center
        self.y = y  # y-coordiante of center
        self.direction = direction  # direction of bullet
        self.velocity = velocity  # velocity of bullet
        self.radius = radius  # radius of bullet
        self.color = color  # color of bullet
        self.reach = reach  # distance the bullet can reach
        self.alive = True  # if bullet is there
        self.shooter = shooter  # Robot who shot this bullet

    def update_bullet(self, map: Map, camera: Camera) -> None:
        # update bullet position and reach
        direction_rad = math.radians(self.direction)
        x = self.velocity * math.cos(direction_rad)
        y = self.velocity * math.sin(direction_rad)
        self.x += x
        self.y += y
        self.reach -= x + y

        # stop bullet, if its outside of the screen
        width = config.COLUMNS * config.TILE_SIZE
        height = config.ROWS * config.TILE_SIZE
        if self.x < 0 or self.x > width:
            self.alive = False
        if self.y < 0 or self.y > height:
            self.alive = False

        # stop bullet, if it hits wall or at end of reach
        current_col = int(self.x / config.TILE_SIZE)
        current_row = int(self.y / config.TILE_SIZE)
        if map.get_tile_type(current_col, current_row) == "wall":
            self.alive = False
        if self.reach <= 0:
            self.alive = False

        # draw bullet
        draw_x, draw_y = camera.apply(int(self.x), int(self.y))
        pygame.draw.circle(camera.surface, self.color, (draw_x, draw_y), self.radius)
