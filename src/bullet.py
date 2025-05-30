import pygame
import math
import config
from robot import Robot
from arena import Arena

velocity = 5


class Bullet:
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        direction: float,
        radius: int,
        color: tuple[int, int, int],
    ):
        self.screen = screen
        self.x = x  # x-coordiante of center
        self.y = y  # y-coordiante of center
        self.direction = direction  # direction of bullet
        self.velocity = velocity  # velocity of bullet
        self.radius = radius  # radius of bullet
        self.color = color  # color of bullet
        self.alive = True  # if bullet is there

    def update_bullet(self, arena: Arena) -> None:
        # update bullet position
        direction_rad = math.radians(self.direction)
        self.x += self.velocity * math.cos(direction_rad)
        self.y += self.velocity * math.sin(direction_rad)

        # stop bullet, if its outside of the screen
        width = config.COLUMNS * config.TILE_SIZE
        height = config.ROWS * config.TILE_SIZE
        if self.x < 0 or self.x > width:
            self.alive = False
        if self.y < 0 or self.y > height:
            self.alive = False

        # stop bullet, if it hits wall
        current_col = int(self.x / config.TILE_SIZE)
        current_row = int(self.y / config.TILE_SIZE)
        if arena.grid[current_row][current_col] == "wall":
            self.alive = False

        # draw bullet
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def collision_with_robots(self, shooter: Robot, robots: list[Robot]) -> None:
        for robot in robots:
            if robot is shooter:  # except for robot which shot the bullet
                continue
            dist_x = abs(robot.x - self.x)
            dist_y = abs(robot.y - self.y)
            dist = math.sqrt(dist_x**2 + dist_y**2)
            max_dist = robot.r + self.radius
            if dist < max_dist:
                self.alive = False
                robot.lives = robot.lives - 1
