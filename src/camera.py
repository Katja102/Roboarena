import pygame


class Camera:
    def __init__(self, camera_surface_width: int, camera_surface_height: int):
        self.camera_surface_width = camera_surface_width
        self.camera_surface_height = camera_surface_height
        self.offset_x = 0
        self.offset_y = 0
        self.surface = pygame.Surface(
            (self.camera_surface_width, self.camera_surface_height)
        )

    def follow(self, target_x: int, target_y: int):
        """Centers the camera on the target position (the player)"""
        self.offset_x = target_x - self.camera_surface_width // 2
        self.offset_y = target_y - self.camera_surface_height // 2

    def apply(self, x: int, y: int) -> tuple[int, int]:
        """Converts world coordinates to screen coordinates"""
        return x - self.offset_x, y - self.offset_y
