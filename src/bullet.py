import pygame
import math
import config
from robot import Robot

velocity = 5


class Bullet:
    def __init__(
            self,
            screen: pygame.Surface,
            startx: int,
            starty: int,
            direction: float,
            radius: int,
            color: tuple[int, int, int]
        ):
            self.screen = screen
            self.startx = startx
            self.starty = starty
            self.direction = direction
            self.currentx = startx
            self.currenty = starty
            self.velocity = velocity
            self.radius = radius
            self.color = color
            self.alive = True

    def update_bullet(self) -> None:
        # update bullet position
        direction_rad = math.radians(self.direction)
        self.currentx += self.velocity * math.cos(direction_rad)
        self.currenty += self.velocity * math.sin(direction_rad)

        # stop bullet, if its outside of the screen
        width = config.COLUMNS * config.TILE_SIZE
        height = config.ROWS * config.TILE_SIZE
        if self.currentx < 0 or self.currentx > width:
             self.alive = False
        if self.currenty < 0 or self.currenty > height:
             self.alive = False

        # stop bullet, if it hits wall
        # To-Do

        # draw bullet
        pygame.draw.circle(self.screen, self.color, (self.currentx, self.currenty), self.radius)

    def collision_with_robots(self, shooter: Robot, robots: list[Robot]) -> None:
         for robot in robots:
              if robot is shooter:
                   continue
              dist_x = abs(robot.x - self.currentx)
              dist_y = abs(robot.y - self.currenty)
              dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
              max_dist = robot.r + self.radius
              if dist < max_dist:
                   self.alive = False
                   robot.lives = robot.lives - 1


