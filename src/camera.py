import pygame


class Camera:
    def __init__(
        self,
        camera_surface_width: int,
        camera_surface_height: int,
        map_pixel_width: int,
        map_pixel_height: int,
    ):
        self.zoom: float = 1.3  # Current zoom level
        self.camera_surface_width = camera_surface_width
        self.camera_surface_height = camera_surface_height
        self.map_pixel_width = map_pixel_width  # Total map width in pixels
        self.map_pixel_height = map_pixel_height  # Total map height in pixels
        self.offset_x = 0
        self.offset_y = 0
        self.center_x = 0  # Camera center X in world coords
        self.center_y = 0  # Camera center Y in world coords
        self.surface = pygame.Surface(
            (self.camera_surface_width, self.camera_surface_height)
        )

    def follow_dynamic_center(self, robots: list, player):
        """
        follow the center between all robots and the player
        adjust zoom based on average distance to enemies
        hold camera inside map boundaries
        """
        # Add player again to robots in order to pull the center toward the player
        bots_with_duplicate_player = robots + [player]

        if not bots_with_duplicate_player:
            cx, cy = player.x, player.y
            avg_distance = 0
        else:
            # Average position of all bots
            sum_x = sum(bot.x for bot in bots_with_duplicate_player)
            sum_y = sum(bot.y for bot in bots_with_duplicate_player)
            n = len(bots_with_duplicate_player)
            cx = sum_x / n
            cy = sum_y / n

            # Average distance from enemies to player
            distances = [
                ((bot.x - player.x) ** 2 + (bot.y - player.y) ** 2) ** 0.5
                for bot in robots
            ]
            avg_distance = sum(distances) / len(distances) if distances else 0

        # Set initial center directly
        if self.center_x == 0 and self.center_y == 0:
            self.center_x = cx
            self.center_y = cy

        # Smoothly follow the target center
        self.center_x += (cx - self.center_x) * 0.1
        self.center_y += (cy - self.center_y) * 0.1

        # Compute Offset based on center + zoom
        half_width = self.camera_surface_width / (2 * self.zoom)
        half_height = self.camera_surface_height / (2 * self.zoom)
        self.offset_x = int(self.center_x - half_width)
        self.offset_y = int(self.center_y - half_height)

        # Dynamic zoom based on distances
        avg_distance = max(20, min(avg_distance, 800))

        # Zoom range
        zoom_near = 1.5
        zoom_far = 0.6

        # Zoom interpolation [0, 1]
        norm_dist = (avg_distance - 100) / 700
        norm_dist = max(0.0, min(norm_dist, 1.0))
        target_zoom = zoom_near - norm_dist * (zoom_near - zoom_far)
        self.zoom += (target_zoom - self.zoom) * 0.1

        # Hold Camera inside the map
        max_offset_x = self.map_pixel_width - (self.camera_surface_width / self.zoom)
        max_offset_y = self.map_pixel_height - (self.camera_surface_height / self.zoom)
        self.offset_x = max(0, min(self.offset_x, int(max_offset_x)))
        self.offset_y = max(0, min(self.offset_y, int(max_offset_y)))

    def apply(self, x: int, y: int) -> tuple[int, int]:
        """Converts world coordinates to screen coordinates"""
        screen_x = (x - self.offset_x) * self.zoom
        screen_y = (y - self.offset_y) * self.zoom
        return int(screen_x), int(screen_y)

    def set_zoom_to(self, value: float):
        # Set zoom level directly limited between 0.8 and 3.0.

        self.zoom = max(0.8, min(value, 3.0))
