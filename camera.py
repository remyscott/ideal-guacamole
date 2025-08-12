from numpy import array, float64
from pygame import surface

class Camera():
    def __init__(self, position, resolution:tuple):
        self.zoom_factor = 40
        self.pos = array(position, float64)
        self.screen = surface.Surface(resolution)
        
    def get_rendered_screen(self, characters):
        self.screen.fill((255,220,200))
        
        for character in characters:
            character_render = character.get_render(self.zoom_factor)
            self.screen.blit(character_render, self.pos_to_screenspace(character.pos, character.camera_offset))
        
        return(self.screen)
    def pos_to_screenspace(self, position, offset):
        camera_relative_position = (position+offset - self.pos) * self.zoom_factor
        return(camera_relative_position)