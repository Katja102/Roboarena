import pygame
import math
import os


class RobotRenderer:
    def __init__(self, camera_surface):
        self.camera_surface = camera_surface
        # -- Animation system explanation --

        # self.animations stores animation frames for each robot type
        # ( "Spider", "Tank",..)

        # This allows different robot types to load their own frame sets

        # self.frame_indices stores the current animation frame index
        # for each robot instance

        # Multiple robots of the same type may be animated independently
        # -> each needs their own index

        # self.timers stores a timer for each robot instance
        # This controls when to advance the animation frame (based on frame_duration)

        # We use dictionaries (robot -> value) so that:
        # -> each robot has its own independent animation state (frame + timer)

        self.animations: dict[str, list[pygame.Surface]] = {}
        self.frame_indices: dict[object, int] = {}
        self.timers: dict[object, float] = {}
        self.frame_duration = 0.3  # seconds per frame

        # Load animation frames for each robot type
        self.load_robot_type("Spider")
        self.load_robot_type("Tank")

    def load_robot_type(self, robot_type: str):
        frames = []
        base_path = f"../resources/{robot_type}"
        for i in range(1, 5):
            img = pygame.image.load(
                os.path.join(base_path, f"d{i}.png")
            ).convert_alpha()
            frames.append(img)
        self.animations[robot_type] = frames

    def update_animation(self, robot, dt):
        if not robot.is_moving:
            self.frame_indices[robot] = 0  # reset to first frame (default sprite)
            self.timers[robot] = 0.0
            return

        # Only animate if conditions match (-> if Spider moves for example)
        if not robot.is_moving:
            return

        if robot not in self.frame_indices:
            self.frame_indices[robot] = 0
            self.timers[robot] = 0.0

        self.timers[robot] += dt
        if self.timers[robot] >= self.frame_duration:
            self.timers[robot] = 0.0
            self.frame_indices[robot] = (self.frame_indices[robot] + 1) % len(
                self.animations[robot.robot_type]
            )

    def draw(self, robot, camera, dt):
        """Renders the robot sprite (or default shape), eyes,
        life count and power bar using the camera system"""

        self.update_animation(robot, dt)

        # Animated sprite
        if robot.robot_type in self.animations:
            frame = self.animations[robot.robot_type][self.frame_indices.get(robot, 0)]
            rotated_image = pygame.transform.rotozoom(frame, -robot.alpha, 1.0)
            rect = rotated_image.get_rect(center=camera.apply(robot.x, robot.y))
            self.camera_surface.blit(rotated_image, rect)
        else:
            # Default body
            pygame.draw.circle(
                self.camera_surface,
                robot.color,
                camera.apply(robot.x, robot.y),
                robot.r,
            )

            # Eyes
            eye_radius = robot.r * 0.1
            eye_offset_deg = 30
            eye_offset_rad = math.radians(eye_offset_deg)
            alpha_rad = math.radians(robot.alpha)
            eye_distance = robot.r * 0.6
            left_eye = (
                robot.x + eye_distance * math.cos(alpha_rad - eye_offset_rad),
                robot.y + eye_distance * math.sin(alpha_rad - eye_offset_rad),
            )
            right_eye = (
                robot.x + eye_distance * math.cos(alpha_rad + eye_offset_rad),
                robot.y + eye_distance * math.sin(alpha_rad + eye_offset_rad),
            )
            pygame.draw.circle(
                self.camera_surface, (0, 0, 0), camera.apply(*left_eye), eye_radius
            )
            pygame.draw.circle(
                self.camera_surface, (0, 0, 0), camera.apply(*right_eye), eye_radius
            )

        # Lives
        font = pygame.font.SysFont("Arial", robot.r, False, False)
        number = font.render(str(robot.lives), True, (0, 0, 0))
        nrect = number.get_rect()
        lives_x, lives_y = camera.apply(robot.x, robot.y)
        lives_x -= nrect.centerx
        lives_y -= nrect.centery
        self.camera_surface.blit(number, [lives_x, lives_y])

        # Power bar
        power_height = robot.r / 2
        power_width = robot.r * 2
        power_x, power_y = camera.apply(robot.x - robot.r, robot.y + (1.5 * robot.r))
        pygame.draw.rect(
            self.camera_surface,
            (255, 255, 255),
            pygame.Rect(power_x, power_y, power_width, power_height),
            2,
        )
        fill_width = power_width * (robot.power / 100)
        pygame.draw.rect(
            self.camera_surface,
            (0, 200, 0),
            pygame.Rect(power_x, power_y, fill_width, power_height),
        )
