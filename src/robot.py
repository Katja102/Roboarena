import pygame
import config
from bullet import Bullet
import math
import random
from map import Map

# Constants
ice_acceleration: float = 2
sand_acceleration: float = 1 / 2

# Recharge-rate (how much power will be recharged every frame)
recharge_rate: float = 0.05


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
        robot_type: str = "",
    ):
        self.screen = screen
        self.x = x  # x-coordiante of center
        self.y = y  # y-coordinate of center
        self.r = radius  # radius of circle
        self.alpha = direction % 360  # direction of the robot in degree
        self.color = color  # color of the robot
        self.v = speed * config.ZOOM  # current acceleration for moving
        self.v_alpha = speed_alpha * config.ZOOM  # current acceleration for turning
        self.speed = speed * config.ZOOM  # speed for moving
        self.speed_alpha = speed_alpha * config.ZOOM  # speed for turning
        self.lives = 3  # current lives of the robot
        self.last_shot_time = 0  # time of last shot
        self.shot_break_duration = 2000  # min duration of break between shots
        self.power = 100  # current power for attacks
        self.in_bush = False  # Whether the robot is currently standing in a bush tile
        self.bush_tiles = (
            []
        )  # List of bush tile positions robot is currently overlapping
        self.robot_type = robot_type
        self.is_moving = False

    # Lets the player move the robot on map
    def update_player(
        self,
        robots: list["Robot"],
        game_map: Map,
        walls: list[pygame.Rect],
        bullets: list[Bullet],
    ) -> None:
        # Check for effect
        self.map_effects(game_map, robots)
        self.robot_collision(robots, walls, game_map)

        # Update player position based on key inputs
        keys = pygame.key.get_pressed()

        x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.v
        y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.v
        self.move_if_no_walls(x, y, walls, game_map)
        self.alpha += (keys[pygame.K_d] - keys[pygame.K_a]) * self.v_alpha
        self.alpha = self.alpha % 360

        self.getting_shot(bullets)

        # recharge power
        if self.power < 100:
            self.power += recharge_rate

        # check, if user used a key for shooting
        if keys[pygame.K_s]:
            self.shoot(bullets)

        # check, if robot is moving
        keys = pygame.key.get_pressed()
        self.is_moving = any(
            [
                keys[pygame.K_UP],
                keys[pygame.K_DOWN],
                keys[pygame.K_LEFT],
                keys[pygame.K_RIGHT],
                keys[pygame.K_a],
                keys[pygame.K_d],
            ]
        )

    # Lets a robot follow another robot
    def update_enemy(
        self,
        goal: "Robot | None",
        robots: list["Robot"],
        game_map: Map,
        walls: list[pygame.Rect],
        bullets: list[Bullet],
    ) -> None:
        # Check for effect
        self.map_effects(game_map, robots)
        self.robot_collision(robots, walls, game_map)

        # Check for goal
        if not goal:
            return None

        # Move towards a goal position
        x_to_goal = goal.x - self.x
        y_to_goal = goal.y - self.y
        x = math.copysign(self.v, x_to_goal)
        y = math.copysign(self.v, y_to_goal)
        self.move_if_no_walls(x, y, walls, game_map, check_for_lava=True)
        self.robot_collision(robots, walls, game_map)

        # Adjust rotation to face the goal
        rad_to_goal = math.atan2(y_to_goal, x_to_goal)
        angle_to_goal = (math.degrees(rad_to_goal) + 180) % 360

        # Invert direction if shortest rotation is the other way
        if angle_to_goal < self.alpha:
            if abs(angle_to_goal - self.alpha) > 180:
                angle_to_goal *= -1
        else:
            if abs(angle_to_goal - self.alpha) < 180:
                angle_to_goal *= -1
        self.alpha += math.copysign(self.v_alpha, angle_to_goal)
        self.alpha = self.alpha % 360

        # check if self gets shot
        self.getting_shot(bullets)

        # recharge power
        if self.power < 100:
            self.power += recharge_rate

        # shoot if angle to goal is under 10°
        angle_diff = abs(abs(angle_to_goal - 180) - self.alpha) % 360
        if (angle_diff <= 10) or (angle_diff >= 350):
            self.shoot(bullets)

        # avoid being in range of other robots
        self.move_if_in_range(robots, walls, game_map)
        self.robot_collision(robots, walls, game_map)

        # # check, if robot NPC is moving
        self.is_moving = (
            abs(goal.x - self.x) > 0.5
            or abs(goal.y - self.y) > 0.5
            or abs(angle_to_goal - self.alpha) > 1
        )

    # React to collisions with other robots
    def robot_collision(
        self, robots: list["Robot"], walls: list[pygame.Rect], game_map: Map
    ) -> None:
        if len(robots) > 1:
            (dist, robot) = self.robot_dist(robots)[0]
            if dist <= 0:
                rad_to_goal = math.atan2(robot.y - self.y, robot.x - self.x)
                angle_to_goal = math.degrees(rad_to_goal) + 180 % 360
                angle_away = angle_to_goal
                x = 10 * math.cos(angle_away * math.pi / 180)
                y = 10 * math.sin(angle_away * math.pi / 180)
                self.move_if_no_walls(x, y, walls, game_map)

    # Detect distances to other robots
    def robot_dist(self, robots: list["Robot"]) -> list[tuple[float, "Robot"]]:
        dist_robot: list[tuple[float, Robot]] = []
        for robot in robots:
            if robot != self:
                x_to_robot = robot.x - self.x
                y_to_robot = robot.y - self.y
                dist = (
                    math.sqrt((x_to_robot) ** 2 + (y_to_robot) ** 2) - self.r - robot.r
                )
                dist_robot.append((dist, robot))
        dist_robot = sorted(dist_robot, key=lambda x: x[0])
        return dist_robot

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
                touching_tiles.append((i, j))
        return touching_tiles

    # Get the textures of the tiles touched by the robot
    def touched_textures(self, game_map: Map) -> list[str]:
        touched_textures = []
        for [i, j] in self.touched_tiles():
            touched_textures.append(game_map.get_tile_type(i, j))
        return touched_textures

    # Effect for robot from map
    def map_effects(self, game_map: Map, robots: list["Robot"]) -> None:
        touched_textures = self.touched_textures(game_map)
        if "ice" in touched_textures:
            self.v = self.speed * ice_acceleration
            self.v_alpha = self.speed_alpha * ice_acceleration
        elif "sand" in touched_textures:
            self.v = self.speed * sand_acceleration
            self.v_alpha = self.speed_alpha * sand_acceleration
        elif "wall" in touched_textures:
            pass
        else:
            self.v = self.speed
            self.v_alpha = self.speed_alpha
        if "lava" in touched_textures:
            self.get_spawn_position(game_map, robots)
            self.lives -= 1

        if "bush" in touched_textures:
            self.in_bush = True
            self.bush_tiles = []
            for [i, j] in self.touched_tiles():
                if game_map.get_tile_type(i, j) == "bush":
                    self.bush_tiles.append((i, j))
        else:
            self.in_bush = False
            self.bush_tiles = []

    # Get random spawn position
    def get_spawn_position(
        self, game_map: Map, robots: list["Robot"]
    ) -> tuple[int, int]:
        # Get random position
        position_x = random.randint(
            2 * config.TILE_SIZE + self.r, (config.COLUMNS - 2) * config.TILE_SIZE
        )
        position_y = random.randint(
            2 * config.TILE_SIZE + self.r, (config.ROWS - 2) * config.TILE_SIZE
        )
        # Check for distance to other robots
        self.x = position_x
        self.y = position_y
        max_dist = math.hypot(
            config.TILE_SIZE * (config.ROWS - 2),
            config.TILE_SIZE * (config.COLUMNS - 2),
        )
        min_dist = max_dist / (len(robots) + 1)
        if self.robot_dist(robots)[0][0] > min_dist:
            # Check for tiles to avoid walls, lava and bush
            touched_textures = self.touched_textures(game_map)
            if (
                ("lava" not in touched_textures)
                and ("wall" not in touched_textures)
                and ("bush" not in touched_textures)
            ):
                return (position_x, position_y)
        # Try again
        return self.get_spawn_position(game_map, robots)

    # moves robot if new position not in wall
    def move_if_no_walls(
        self,
        x: float,
        y: float,
        walls: list[pygame.Rect],
        game_map: Map,
        check_for_lava: bool = False,
    ) -> None:
        xnew = self.x + x
        ynew = self.y + y
        newRect = pygame.Rect(xnew - self.r, ynew - self.r, self.r * 2, self.r * 2)
        # moves robot to direct wanted path if no wall
        if newRect.collidelist(walls) == -1:
            self.x = xnew
            self.y = ynew
            if check_for_lava:
                touched_textures = self.touched_textures(game_map)
                if "lava" in touched_textures:
                    self.x -= x
                    self.y -= y
                check_for_lava = False
        # to avoid not moving at all when goal is behind wall
        else:
            # check and move if only in x direction is no wall
            xnew = self.x + x
            ynew = self.y
            newRect = pygame.Rect(xnew - self.r, ynew - self.r, self.r * 2, self.r * 2)
            if newRect.collidelist(walls) == -1:
                self.x = xnew
                self.y = ynew
            else:
                # check and move if only in y direction is no wall
                xnew = self.x
                ynew = self.y + y
                newRect = pygame.Rect(
                    xnew - self.r, ynew - self.r, self.r * 2, self.r * 2
                )
                if newRect.collidelist(walls) == -1:
                    self.x = xnew
                    self.y = ynew

    def shoot(self, bullets: list[Bullet]):
        current_time = pygame.time.get_ticks()
        # make sure there is a break between the shots
        if current_time - self.last_shot_time < self.shot_break_duration:
            return None
        # make sure there is enough power
        if self.power <= 20:
            return None
        # shoot, if there is enough time and power

        alpha_rad = math.radians(self.alpha)
        start_x = self.x + self.r * math.cos(alpha_rad)  # start outsinde of the robot
        start_y = self.y + self.r * math.sin(alpha_rad)
        bullet = Bullet(
            int(start_x),
            int(start_y),
            self.alpha,
            5,
            (0, 0, 0),
            shooter=self,
        )  # create bullet
        self.last_shot_time = current_time  # update time of last shot
        self.power -= 20  # update power
        bullets.append(bullet)

    # checks and react if robot is shot
    def getting_shot(self, bullets: list[Bullet]) -> None:
        for bullet in bullets:
            if self is bullet.shooter:  # except for robot which shot the bullet
                continue
            dist_x = abs(bullet.x - self.x)
            dist_y = abs(bullet.y - self.y)
            dist = math.sqrt(dist_x**2 + dist_y**2)
            max_dist = bullet.radius + self.r
            if dist < max_dist:
                bullet.alive = False
                self.lives = self.lives - 1

    # helper-function to get list of robots with probability corresponding to its distance
    def dist_to_prob(
        self, dist_robot: list[tuple[float, "Robot"]]
    ) -> list[tuple[float, "Robot"]]:
        prob_robot: list[tuple[float, "Robot"]] = []
        total_dist: float = sum(d for d, r in dist_robot)
        for dist, robot in dist_robot:
            prob: float = total_dist / dist
            prob_robot.append((prob, robot))
        return prob_robot

    # helper-function to get list of robots with corresponding distance
    def get_robot_with_distance_prob(
        self, game_map: Map, robots: list["Robot"]
    ) -> "None | Robot":
        potential_goals: list["Robot"] = []
        for robot in robots:
            if "bush" not in robot.touched_textures(game_map) and robot is not self:
                potential_goals.append(robot)
        if len(potential_goals) > 0:
            dist_robot: list[tuple[float, "Robot"]] = self.robot_dist(potential_goals)
            prob_robot: list[tuple[float, "Robot"]] = self.dist_to_prob(dist_robot)
            robot: "Robot" = random.choices(
                [r for p, r in prob_robot], weights=[p for p, r in prob_robot], k=1
            )[0]
            return robot
        return None

    # Avoid if in range of other robots
    def move_if_in_range(
        self, robots: list["Robot"], walls: list[pygame.Rect], game_map: Map
    ) -> None:
        for robot in robots:
            if robot == self:
                continue
            rad_to_robot = math.atan2(robot.y - self.y, robot.x - self.x)
            angle_to_robot = math.degrees(rad_to_robot) + 180 % 360
            angle_diff = abs(abs(angle_to_robot) - robot.alpha) % 360
            if (angle_diff <= 10) or (angle_diff >= 350):  # in range of robot
                x_to_goal = robot.x - self.x
                y_to_goal = robot.y - self.y
                if abs(y_to_goal) <= 0.5:
                    x = math.copysign(0, y_to_goal)
                else:
                    x = math.copysign(self.v, y_to_goal)
                if abs(x_to_goal) <= 0.5:
                    y = math.copysign(self.v, x_to_goal * -1)
                else:
                    y = math.copysign(0, x_to_goal * -1)
                self.move_if_no_walls(x, y, walls, game_map)  # move to side
