import pygame
import math
import os
import config

# Constante definitions
POWER_BAR_COLOR : tuple[int, int, int] = (0, 180, 220)
LIFE_BAR_COLORS: dict[str, tuple[int, int, int]] = {
    "green": (0, 220, 0),
    "yellow": (220, 210, 0),
    "red": (210, 0, 0),
}
BAR_BACKGROUND_DIM = 120



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

    def draw_text_with_outline(self, font, text, x, y, color=(255, 255, 255), outline_color=(0, 0, 0)):
        offsets = [  # outline in 8 directions
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)
        ]

        # draw black outline first
        for offset_x, offset_y in offsets:
                    outline = font.render(text, True, outline_color)
                    self.camera_surface.blit(outline, (x + offset_x, y + offset_y))
        # Draw main text
        main_text = font.render(text, True, color)
        self.camera_surface.blit(main_text, (x, y))


    def draw(self, robot, camera, dt):
        """Renders the robot sprite (or default shape), eyes,
        life count and power bar using the camera system"""

        self.update_animation(robot, dt)

        if robot.robot_type in self.animations:
            # Get current animation frame
            frame = self.animations[robot.robot_type][self.frame_indices.get(robot, 0)]

            # Step 1: Scale the image first to TILE_SIZE
            target_size = config.TILE_SIZE
            scaled_image = pygame.transform.smoothscale(frame, (target_size, target_size))

            # Step 2: Rotate after scaling
            rotated_image = pygame.transform.rotate(scaled_image, -robot.alpha)

            # Step 3: Center the rotated image at the robot's position
            rect = rotated_image.get_rect(center=camera.apply(robot.x, robot.y))

            # Step 4: Draw on the camera surface
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

        # Power bar
        power_height = config.TILE_SIZE * 0.15
        power_width = config.TILE_SIZE
        power_x, power_y = camera.apply(robot.x - robot.r, robot.y + (1.7 * robot.r))
        fill_width = power_width * (robot.power / 100)

        # background color (with minimum dim)
        power_ratio = robot.power / 100
        raw_dim = int((1 - power_ratio) * BAR_BACKGROUND_DIM / 2)
        dim = max(raw_dim, 35)
        r, g, b = POWER_BAR_COLOR
        bg_color_power = (max(r - dim, 0), max(g - dim, 0), max(b - dim, 0))
        bg_power_rect = pygame.Rect(power_x, power_y, power_width, power_height)

        # Draw background bar
        pygame.draw.rect(self.camera_surface, bg_color_power, bg_power_rect)

        # Draw outline for background bar
        bg_outline_color = (
            min(bg_color_power[0] + 20, 255),
            min(bg_color_power[1] + 20, 255),
            min(bg_color_power[2] + 20, 255)
        )
        pygame.draw.rect(self.camera_surface, bg_outline_color, bg_power_rect, 4)

        # Draw fill bar
        pygame.draw.rect(
            self.camera_surface,
            POWER_BAR_COLOR,
            pygame.Rect(power_x, power_y, fill_width, power_height)
        )

        # Draw outline for fill bar
        r, g, b = POWER_BAR_COLOR
        highlight_color = (
            min(r + 20, 255),
            min(g + 20, 255),
            min(b + 20, 255)
        )
        pygame.draw.rect(
            self.camera_surface,
            highlight_color,
            pygame.Rect(power_x, power_y, fill_width, power_height),
            4
        )

        # Draw power value text
        font = pygame.font.SysFont("Arial", int(power_height * 1.5), bold=True)
        text = str(int(robot.power))
        power_number = font.render(text, True, (255, 255, 255))
        p_nrect = power_number.get_rect()
        power_text_x = power_x + (power_width - p_nrect.width) // 2
        power_text_y = power_y + (power_height - p_nrect.height) // 2

        if config.SHOW_STATS:
            self.draw_text_with_outline(font, text, power_text_x, power_text_y)

        # Draw power icon (lightning)
        icon_power = pygame.transform.scale(config.ICONS["power"], (int(power_height + 4), int(power_height + 4)))
        icon_x = power_x - icon_power.get_width() - 5
        icon_y = power_y
        self.camera_surface.blit(icon_power, (icon_x, icon_y))


        # --- Life bar (above power bar) ---
        max_life_height = power_height  # same height as power bar
        max_life_widht = power_width  # same width as power bar
        fill_life_width = max_life_widht * (robot.hp / 100)
        life_x = power_x
        bar_spacing = config.TILE_SIZE * 0.2  # vertical offset
        life_y = power_y - bar_spacing

        # Choose fill color based on HP
        if robot.hp >= 50:
            bar_color = LIFE_BAR_COLORS["green"]
        elif robot.hp >= 20:
            bar_color = LIFE_BAR_COLORS["yellow"]
        else:
            bar_color = LIFE_BAR_COLORS["red"]

        # Background color (darker based on HP, with minimum dimming)
        hp_ratio = robot.hp / 100
        raw_dim_factor = int((1 - hp_ratio) * BAR_BACKGROUND_DIM)
        dim_factor = max(raw_dim_factor, 10)
        r, g, b = bar_color
        bg_color_rgb = (max(r - dim_factor, 0), max(g - dim_factor, 0), max(b - dim_factor, 0))
        bg_rect = pygame.Rect(life_x, life_y, max_life_widht, max_life_height)

        # Draw background
        pygame.draw.rect(self.camera_surface, bg_color_rgb, bg_rect)

        # Draw outline for background bar
        bg_outline_color = (
            min(bg_color_rgb[0] + 20, 255),
            min(bg_color_rgb[1] + 20, 255),
            min(bg_color_rgb[2] + 20, 255)
        )
        pygame.draw.rect(self.camera_surface, bg_outline_color, bg_rect, 4)  # thickness = 4

        # Draw fill bar
        pygame.draw.rect(
            self.camera_surface,
            bar_color,
            pygame.Rect(life_x, life_y, fill_life_width, max_life_height),
        )

        # Draw outline for fill bar
        r, g, b = bar_color
        highlight_color = (
            min(r + 40, 255),
            min(g + 40, 255),
            min(b + 40, 255)
        )

        pygame.draw.rect(
            self.camera_surface,
            highlight_color,
            pygame.Rect(life_x, life_y, fill_life_width, max_life_height),
            4
        )

        # Draw text (HP number)
        life_text = str(int(robot.hp))
        l_nrect = font.render(life_text, True, (0, 0, 0)).get_rect()  # use same font as power bar
        text_x = life_x + (max_life_widht - l_nrect.width) // 2
        text_y = life_y + (max_life_height - l_nrect.height) // 2

        # Only show HP text if SHOW_STATS is active
        if config.SHOW_STATS:
            self.draw_text_with_outline(font, life_text, text_x, text_y)


        # Draw life icon (heart)
        icon_size = max_life_height  # gleiche Höhe wie die Leiste
        icon_heart = pygame.transform.scale(config.ICONS["heart"], (int(icon_size + 3), int(icon_size + 3)))
        icon_x = life_x - icon_heart.get_width() - 5  # 5 Pixel Abstand nach links
        icon_y = life_y
        self.camera_surface.blit(icon_heart, (icon_x, icon_y))
