from pathlib import Path
from pygame.locals import *
import pickle
from random import randint


class Default_settings():
    def __init__(self):
        self.FULLSCREEN = False
        self.DISPLAY_WIDTH = 1080
        self.DISPLAY_HEIGHT = 720
        self.SCREEN_WIDTH = 1080
        self.SCREEN_HEIGHT = 720
        self.FRAMERATE = 120
        self.CAMERA_ZOOM_FACTOR = 40

class Settings_functions():
    def get_settings():
        settings_path = Path('data/user/settings.bin')

        settings_file = open(settings_path, 'rb')
        settings = pickle.load(settings_file)
        settings_file.close()


        return(settings)

    def reset_settings():
    
        settings_path = Path('data/user/settings.bin')
        settings_file = open(settings_path, 'wb')
        pickle.dump(Default_settings(), settings_file)
        settings_file.close()