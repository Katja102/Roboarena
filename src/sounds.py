import pygame

class Sounds:
    def __init__(self, file_path: str):
        pygame.mixer.init()
        self.sounds = {
            "wall_hit_sound": pygame.mixer.Sound(f"{file_path}/wall_hit.ogg"),
            "lava_sound": pygame.mixer.Sound(f"{file_path}/lava.wav"),
            "ice_sound": pygame.mixer.Sound(f"{file_path}/cartoon-slide-whistle-down-1-176647.mp3"),
            "sand_sound": pygame.mixer.Sound(f"{file_path}/sand.wav"),
            "bush_sound": pygame.mixer.Sound(f"{file_path}/bush.ogg"),
            "shot_sound": pygame.mixer.Sound(f"{file_path}/shoot.ogg"),
            "drive_sound": pygame.mixer.Sound(f"{file_path}/drive.mp3"),
            "player_hit_sound": pygame.mixer.Sound(f"{file_path}/player_hit.ogg") 
        }
        self.channel_drive = pygame.mixer.Channel(1)
        self.channel_loop = pygame.mixer.Channel(2)
        self.channel_single = pygame.mixer.Channel(3)
        self.loops = {"bush_sound", "sand_sound", "drive_sound"}
        self.current_loop = None
        self.drive_playing = False
    
    def play_sound(self, action: str):
        if action == "drive_sound" and not self.drive_playing:
            self.channel_drive.play(self.sounds["drive_sound"], loops=-1)
            self.drive_playing = True
        elif action in self.loops:
            if action != self.current_loop:
                self.stop_loop(action)
                if self.drive_playing:
                    self.sounds["drive_sound"].set_volume(0.5)
                if not self.is_playing_anywhere(action):
                    self.channel_loop.play(self.sounds[action], loops=-1)
                self.current_loop = action
        else:
            if not self.is_playing_anywhere(action):
                self.channel_single.play(self.sounds[action], loops=0)

    def stop_loop(self, action: str):
        if action == "drive_sound":
            self.drive_playing = False
            if self.channel_drive.get_busy():
                self.channel_drive.stop()
        if action in self.loops:
            if self.channel_loop.get_busy():
                self.channel_loop.stop()
            self.current_loop = None
            if self.drive_playing:
                self.sounds["drive_sound"].set_volume(1.0)


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
    
    def is_playing_anywhere(self, sound: str):
        for i in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(i)
            if channel.get_sound() == self.sounds[sound] and channel.get_busy():
                return True
        return False

