import pygame


class Sounds:
    def __init__(self):
        pygame.mixer.init()
        # load sounds
        self.sounds = {
            "wall_hit_sound": pygame.mixer.Sound("../resources/sounds/wall_hit.ogg"),
            "lava_sound": pygame.mixer.Sound("../resources/sounds/lava.wav"),
            "ice_sound": pygame.mixer.Sound(
                "../resources/sounds/cartoon-slide-whistle-down-1-176647.mp3"
            ),
            "sand_sound": pygame.mixer.Sound("../resources/sounds/sand.wav"),
            "bush_sound": pygame.mixer.Sound("../resources/sounds/bush.ogg"),
            "shot_sound": pygame.mixer.Sound("../resources/sounds/shoot.ogg"),
            "drive_sound": pygame.mixer.Sound("../resources/sounds/drive.mp3"),
            "player_hit_sound": pygame.mixer.Sound(
                "../resources/sounds/player_hit.ogg"
            ),
        }

        self.channel_drive = pygame.mixer.Channel(1)
        self.channel_loop = pygame.mixer.Channel(2)
        self.channel_single = pygame.mixer.Channel(3)
        self.loops = {"bush_sound", "sand_sound", "drive_sound"}
        self.current_loop = None
        self.drive_playing = False

        self.sounds["drive_sound"].set_volume(0.6)

    def play_sound(self, action: str):
        if action == "drive_sound" and not self.drive_playing:
            self.channel_drive.play(self.sounds["drive_sound"], loops=-1)
            self.drive_playing = True
        elif action in self.loops:
            if action != self.current_loop:
                self.stop_loop(action)
                if self.drive_playing:
                    self.sounds["drive_sound"].set_volume(
                        0.4
                    )  # make drive sound quieter while other loop sound is playing
                if not self.channel_loop.get_busy():
                    self.channel_loop.play(self.sounds[action], loops=-1)
                self.current_loop = action
        else:
            if (
                not self.channel_single.get_busy()
                and not self.channel_single.get_sound == self.sounds[action]
            ):
                if action == "player_hit":
                    self.channel_single.set_volume(0.3)
                else:
                    self.channel_single.set_volume(0.3)
                self.channel_single.play(self.sounds[action], loops=0)

    def stop_loop(self, action: str):
        if action == "drive_sound":
            self.drive_playing = False
            if self.channel_drive.get_busy():
                self.channel_drive.stop()
        if action in self.loops:
            if self.channel_loop.get_busy():
                self.sounds[action].stop()
            self.current_loop = None
            if self.drive_playing:
                self.sounds["drive_sound"].set_volume(0.6)

    def stop_all_sounds(self):
        for sound in self.sounds:
            if sound == "drive_sound" and self.channel_drive.get_busy():
                self.channel_drive.stop()
            elif sound in self.loops and self.channel_loop.get_busy():
                self.channel_loop.stop()
            else:
                if self.channel_single.get_busy():
                    self.channel_single.stop()
            self.current_loop = None
            self.drive_playing = False
