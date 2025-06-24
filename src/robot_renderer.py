import pygame
import config
import math


class RobotRenderer:
    def __init__(self, camera_surface):
        self.camera_surface = camera_surface

    def draw(self, robot, camera):
        # Body
        pygame.draw.circle(
            self.camera_surface, robot.color, camera.apply(robot.x, robot.y), robot.r
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

        # Bush overlay
        if robot.in_bush:
            for i, j in robot.bush_tiles:
                # Calculate visual tile size on camera_surface
                visual_tile_size = self.camera_surface.get_width() // config.COLUMNS

                # Load bush texture and scale it to fit current tile size
                texture = config.TEXTURES["bush"]
                tile = pygame.transform.scale(
                    texture, (visual_tile_size, visual_tile_size)
                )

                # Draw bush overlay at correct map position
                self.camera_surface.blit(
                    tile, camera.apply(i * config.TILE_SIZE, j * config.TILE_SIZE)
                )
