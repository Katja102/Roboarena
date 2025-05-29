import pygame
import math

# Maximum acceleration values
a_max: float = 1
a_alpha_max: float = 1


class Robot:
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        radius: int,
        direction: int,
        color: tuple[int, int, int],
        a: float,
        a_alpha: float
    ):
        self.screen = screen
        self.x = x  # x-coordiante of center
        self.y = y  # y-coordinate of center
        self.r = radius  # radius of circle
        self.alpha = direction  # direction of the robot in degree
        self.color = color  # color of the robot
        self.a = a  # current acceleration for moving
        self.a_alpha = a_alpha  # current acceleration for turning
        self.a_max = a_max  # maximal acceleration for moving
        self.a_alpha_max = a_alpha_max  # maximal acceleration for turning
        self.v = 1  # speed for moving
        self.v_alpha = 1  # speed for turning
        self.lives = 3  # current lives of the robot
        self.last_shot_time = 0  # time of last shot
        self.shot_break_duration = 1000  # min duration of break between shots

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

        # draw lives
        font = pygame.font.SysFont('Arial', self.r, False, False)
        number_writing = font.render(str(self.lives), True, (0,0,0))
        number_rect = number_writing.get_rect() # rectangle with size of number
        lives_x = self.x - number_rect.centerx # place number in the center of robot circle
        lives_y = self.y - number_rect.centery
        self.screen.blit(number_writing, [lives_x, lives_y])


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
        if self.lives > 0:
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

    def shoot(self):
        current_time = pygame.time.get_ticks()
        # make sure there is a break between the shots
        if current_time - self.last_shot_time < self.shot_break_duration:
            return None
        # shoot, if there is enough time
        from bullet import Bullet
        alpha_rad = math.radians(self.alpha)
        # start outsinde of the robot
        start_x = self.x + self.r * math.cos(alpha_rad)
        start_y = self.y + self.r * math.sin(alpha_rad)
        bullet = Bullet(self.screen, int(start_x), int(start_y), self.alpha, 5 , (0,0,0)) # create bullet
        self.last_shot_time = current_time
        return bullet

