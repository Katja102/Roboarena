import pygame
import math

# Maximum acceleration values
a_max = 1
a_alpha_max = 1


class Robot:
    def __init__(
        self,
        screen,
        x: int,
        y: int,
        radius: int,
        direction: int,
        color: tuple[int, int, int],
        a: float,
        a_alpha: float,
    ):
        self.screen = screen
        self.x = x  # x-coordiante of center
        self.y = y  # y-coordinate of center
        self.r = radius  # radius of circle
        self.alpha = direction  # direction of the robot
        self.color = color  # color of the robot
        self.a = a  # current acceleration for moving
        self.a_alpha = a_alpha  # current acceleration for turning
        self.a_max = a_max  # maximal acceleration for moving
        self.a_alpha_max = a_alpha_max  # maximal acceleration for turning
        self.v = 1  # speed for moving
        self.v_alpha = 1  # speed for turning

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

    def update_player(self, robots: list["Robot"]) -> None:
        # Update player position based on key inputs
        self.draw_robot()

        keys = pygame.key.get_pressed()

        self.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.v
        self.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.v
        self.alpha += (keys[pygame.K_d] - keys[pygame.K_a]) * self.v_alpha

        # Check for collisions
        self.robot_collision(robots)

    def update_enemy(self, goal: "Robot", robots: list["Robot"]) -> None:
        # Move towards a goal position
        x_to_goal = goal.x - self.x
        y_to_goal = goal.y - self.y
        self.x += math.copysign(self.v, x_to_goal) / 3
        self.y += math.copysign(self.v, y_to_goal) / 3

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
        self.draw_robot()
        self.robot_collision(robots)

    def move_circle(
        self, point: tuple[int, int], r: int, angle: int, robots: list["Robot"]
    ) -> None:
        # Move in a circle around a point
        self.x = point[0] + r * math.cos(angle * math.pi / 180)
        self.y = point[1] + r * math.sin(angle * math.pi / 180)
        self.alpha = angle + 90  # rotate to face along the circle
        self.draw_robot()
        self.robot_collision(robots)

    def robot_collision(self, robots: list["Robot"]) -> None:
        # Detect and react to collisions with other robots
        for robot in robots:
            if robot != self:
                x_to_robot = robot.x - self.x
                y_to_robot = robot.y - self.y
                dist = math.sqrt((x_to_robot) ** 2 + (y_to_robot) ** 2)
                if dist <= robot.r + self.r:
                    rad_to_goal = math.atan2(y_to_robot, x_to_robot)
                    angle_to_goal = math.degrees(rad_to_goal) + 180 % 360
                    angle_away = angle_to_goal
                    self.x += 10 * math.cos(angle_away * math.pi / 180)
                    self.y += 10 * math.sin(angle_away * math.pi / 180)
