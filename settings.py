from pathlib import Path
from pygame.locals import *
import pickle
from random import randint
from dataclasses import dataclass

@dataclass
class Settings:
    fullscreen: bool = False
    display_width: int = 1080
    display_height: int = 720
    screen_width: int = 1080
    screen_height: int = 720
    framerate: int = 120
    camera_zoom_factor: int = 40

    def get_settings(self):
        settings_path = Path('data/user/settings.bin')

        settings_file = open(settings_path, 'rb')
        settings = pickle.load(settings_file)
        settings_file.close()

        return(settings)

    def reset_settings(self):
        settings_path = Path('data/user/settings.bin')
        settings_file = open(settings_path, 'wb')
        pickle.dump(self, settings_file)
        settings_file.close()


