import pygame
import config
import math
from arena import Arena


class Robot:
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        radius: int,
        direction: int,
        color: tuple[int, int, int],
        speed: float,
        speed_alpha: float,
    ):
        self.screen = screen
        self.x = x  # x-coordiante of center
        self.y = y  # y-coordinate of center
        self.r = radius  # radius of circle
        self.alpha = direction  # direction of the robot
        self.color = color  # color of the robot
        self.v = speed  # current acceleration for moving
        self.v_alpha = speed_alpha  # current acceleration for turning
        self.speed = speed  # speed for moving
        self.speed_alpha = speed_alpha  # speed for turning

    def draw_robot(self) -> None:
        # draw robot (circle)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

        # calculate values for eyes
        eye_radius = self.r * 0.1  # radius of the eyes
        eye_offset_deg = 30  # deviation of angle of the eyes from direction
        eye_offset_rad = math.radians(eye_offset_deg)  # convert to radian
        eye_distance = self.r * 0.6  # distance from center of the robot

        alpha_rad = math.radians(self.alpha)

        # Eye positions (left and right)
        left_eye_x = self.x + (eye_distance * math.cos(alpha_rad - eye_offset_rad))
        left_eye_y = self.y + (eye_distance * math.sin(alpha_rad - eye_offset_rad))
        right_eye_x = self.x + (eye_distance * math.cos(alpha_rad + eye_offset_rad))
        right_eye_y = self.y + (eye_distance * math.sin(alpha_rad + eye_offset_rad))

        # draw eyes
        pygame.draw.circle(self.screen, (0, 0, 0), (left_eye_x, left_eye_y), eye_radius)
        pygame.draw.circle(
            self.screen, (0, 0, 0), (right_eye_x, right_eye_y), eye_radius
        )

    # Lets the player move the robot on map
    def update_player(
        self, robots: list["Robot"], arena: Arena, walls: list[pygame.Rect]
    ) -> None:
        # Check for collisions and effect
        self.map_effects(arena, robots)
        self.robot_collision(robots)

        # Update player position based on key inputs
        keys = pygame.key.get_pressed()

        x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.v
        y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.v
        self.move_if_no_walls(x, y, walls)
        self.alpha += (keys[pygame.K_d] - keys[pygame.K_a]) * self.v_alpha

    # Lets a robot follow another robot
    def update_enemy(
        self,
        goal: "Robot",
        robots: list["Robot"],
        arena: Arena,
        walls: list[pygame.Rect],
    ) -> None:
        # Check for collisions and effect
        self.map_effects(arena, robots)
        self.robot_collision(robots)

        # Move towards a goal position
        x_to_goal = goal.x - self.x
        y_to_goal = goal.y - self.y
        x = math.copysign(self.v, x_to_goal) / 3
        y = math.copysign(self.v, y_to_goal) / 3
        self.move_if_no_walls(x, y, walls)

        # Adjust rotation to face the goal
        rad_to_goal = math.atan2(y_to_goal, x_to_goal)
        angle_to_goal = math.degrees(rad_to_goal) + 180 % 360

        # Invert direction if shortest rotation is the other way
        if angle_to_goal < self.alpha:
            if abs(angle_to_goal - self.alpha) > 180:
                angle_to_goal *= -1
        else:
            if abs(angle_to_goal - self.alpha) < 180:
                angle_to_goal *= -1
        self.alpha += math.copysign(self.v_alpha, angle_to_goal)

    # Move in a circle around a point
    def move_circle(
        self,
        point: tuple[int, int],
        r: int,
        angle: int,
        robots: list["Robot"],
        arena: Arena,
    ) -> None:
        # Check for collisions and effect
        self.map_effects(arena, robots)
        self.robot_collision(robots)

        self.x = point[0] + r * math.cos(angle * math.pi / 180)
        self.y = point[1] + r * math.sin(angle * math.pi / 180)
        self.alpha = angle + 90  # rotate to face along the circle

    # React to collisions with other robots
    def robot_collision(self, robots: list["Robot"]) -> None:
        dist, robot = self.robot_dist(robots)
        if dist <= 0:
            rad_to_goal = math.atan2(robot.y - self.y, robot.x - self.x)
            angle_to_goal = math.degrees(rad_to_goal) + 180 % 360
            angle_away = angle_to_goal
            self.x += 10 * math.cos(angle_away * math.pi / 180)
            self.y += 10 * math.sin(angle_away * math.pi / 180)

    # Detect nearest distance to other robots
    def robot_dist(self, robots: list["Robot"]) -> tuple[float, "Robot"]:
        distance = max(config.COLUMNS, config.ROWS) * config.TILE_SIZE
        nearest_robot: Robot = self
        for robot in robots:
            if robot != self:
                x_to_robot = robot.x - self.x
                y_to_robot = robot.y - self.y
                dist = (
                    math.sqrt((x_to_robot) ** 2 + (y_to_robot) ** 2) - self.r - robot.r
                )
                if dist < distance:
                    distance = dist
                    nearest_robot: Robot = robot
        return (distance, nearest_robot)

    # Get the list of tiles touched by the robot
    def touched_tiles(self) -> list[tuple[int, int]]:
        x_on_tiles = self.x / config.TILE_SIZE
        y_on_tiles = self.y / config.TILE_SIZE
        radius_on_tiles = self.r / config.TILE_SIZE
        x_bounds = [
            math.floor(x_on_tiles - radius_on_tiles),
            math.floor(x_on_tiles + radius_on_tiles),
        ]
        y_bounds = [
            math.floor(y_on_tiles - radius_on_tiles),
            math.floor(y_on_tiles + radius_on_tiles),
        ]
        touching_tiles = []
        for i in range(x_bounds[0], x_bounds[1] + 1):
            for j in range(y_bounds[0], y_bounds[1] + 1):
                touching_tiles.append([i, j])
        return touching_tiles

    # Get the textures of the tiles touched by the robot
    def touched_textures(self, arena: Arena) -> list[str]:
        touched_textures = []
        for [i, j] in self.touched_tiles():
            touched_textures.append(arena.grid[j][i])
        return touched_textures

    # Effect for robot from map
    def map_effects(self, arena: Arena, robots: list["Robot"]) -> None:
        touched_textures = self.touched_textures(arena)
        if "ice" in touched_textures:
            self.v = self.speed * 2
            self.v_alpha = self.speed_alpha * 2
        elif "sand" in touched_textures:
            self.v = self.speed / 2
            self.v_alpha = self.speed_alpha / 2
        elif "wall" in touched_textures:
            pass
        else:
            self.v = self.speed
            self.v_alpha = self.speed_alpha
        self.draw_robot()
        if "lava" in touched_textures:
            pass
        if "bush" in touched_textures:
            for [i, j] in self.touched_tiles():
                if "bush" == arena.grid[j][i]:
                    texture = config.TEXTURES["bush"].convert()
                    tile = pygame.transform.scale(
                        texture, (config.TILE_SIZE, config.TILE_SIZE)
                    )
                    self.screen.blit(tile, (i * config.TILE_SIZE, j * config.TILE_SIZE))

    # moves robot if new position not in wall
    def move_if_no_walls(self, x: float, y: float, walls: list[pygame.Rect]) -> None:
        xnew = self.x + x
        ynew = self.y + y
        newRect = pygame.Rect(xnew - self.r, ynew - self.r, self.r * 2, self.r * 2)
        if newRect.collidelist(walls) == -1:
            self.x = xnew
            self.y = ynew
