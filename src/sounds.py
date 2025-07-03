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
            "spider_sound": pygame.mixer.Sound(
                "../resources/sounds/bs-_swarm-of-roacheswav-14442.mp3"
            ),
            "countdown_sound": pygame.mixer.Sound("../resources/sounds/countdown.ogg"),
            "gameover_sound": pygame.mixer.Sound(
                "../resources/sounds/game_over_bad_chest.wav"
            ),
            "win_sound": pygame.mixer.Sound("../resources/sounds/tadaa-47995.mp3"),
        }

        self.channel_move = pygame.mixer.Channel(1)
        self.channel_loop = pygame.mixer.Channel(2)
        self.channel_single = pygame.mixer.Channel(3)
        self.loops = {"bush_sound", "sand_sound"}
        self.singles = {
            "wall_hit_sound",
            "lava_sound",
            "ice_sound",
            "shot_sound",
            "player_hit_sound",
            "gameover_sound",
            "win_sound",
            "countdown_sound",
        }
        self.current_loop = None
        self.move_playing = False
        self.drive = False
        self.spider = False

        self.sounds["drive_sound"].set_volume(0.6)
        self.sounds["countdown_sound"].set_volume(0.3)

    def play_sound(self, action: str):
        if action == "drive_sound" and not self.move_playing:
            self.channel_move.play(self.sounds["drive_sound"], loops=-1)
            self.move_playing = True
            self.drive = True
        if action == "spider_sound" and not self.move_playing:
            self.channel_move.play(self.sounds["spider_sound"], loops=-1)
            self.move_playing = True
            self.spider = True
        if action in self.loops:
            if action != self.current_loop:
                self.stop_loop(action)
                if self.move_playing:
                    if self.drive:
                        self.sounds["drive_sound"].set_volume(
                            0.4
                        )  # make drive sound quieter while other loop sound is playing
                    if self.spider:
                        self.sounds["spider_sound"].set_volume(
                            0.4
                        )  # make spider sound quieter while other loop sound is playing
                if not self.channel_loop.get_busy():
                    self.channel_loop.play(self.sounds[action], loops=-1)
                self.current_loop = action
        if action in self.singles:
            if (
                not self.channel_single.get_busy()
                and not self.channel_single.get_sound == self.sounds[action]
            ):
                if action == "player_hit":
                    self.channel_single.set_volume(0.3)
                else:
                    self.channel_single.set_volume(1.0)
                self.channel_single.play(self.sounds[action], loops=0)

    def stop_loop(self, action: str):
        if action == "drive_sound":
            self.move_playing = False
            self.drive = False
            if self.channel_move.get_busy():
                self.channel_move.stop()
        if action == "spider_sound":
            self.move_playing = False
            self.spider = False
            if self.channel_move.get_busy():
                self.channel_move.stop()
        if action in self.loops:
            if self.channel_loop.get_busy():
                self.sounds[action].stop()
            self.current_loop = None
            if self.drive:
                self.sounds["drive_sound"].set_volume(0.6)
            if self.spider:
                self.sounds["spider_sound"].set_volume(1.0)

    def stop_all_sounds(self):
        for sound in self.sounds:
            if sound == "drive_sound" or sound == "spider_sound":
                if self.channel_move.get_busy():
                    self.channel_move.stop()
            if sound in self.loops and self.channel_loop.get_busy():
                self.channel_loop.stop()
            if sound in self.singles and self.channel_single.get_busy():
                self.channel_single.stop()
            self.current_loop = None
            self.move_playing = False
            self.drive = False
            self.spider = False
