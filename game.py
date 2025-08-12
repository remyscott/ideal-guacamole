from typing import List
from settings import Settings
from camera import Camera
from game_functions import magnitude
from numpy import array
from dataclasses import dataclass

@dataclass
class GameInputs:
    keys_down: list = []
    key_downs: list = []
    mouse_pos: array = array((0,0))
    mouses_down: list = []

class Game:
    def __init__(self):
        self.settings = Settings()
        self.running = True
        self.camera = Camera((0,0))
        self.entities = []
        self.player_inputs = GameInputs()

    
    def add_entity(self, entity):
        self.entities.append(entity)

    def tick(self):
        self.update_entities()
        self.handle_entity_collisions()
        self.kill_dead_entities()
    
    def update_entities(self):
        for entity in self.entities:
            entity.update(self.player_inputs)

    def handle_entity_collisions(self):
        self.inform_entities_of_collision()
        self.apply_entity_collision_updates()

    def inform_entities_of_collison(self):
        for character_1 in self.entities:
            for character_2 in self.entities:
                if not character_1 == character_2:
                    distance_between_characters = magnitude(character_1.pos - character_2.pos)

                    if distance_between_characters <= character_1.collision_radius + character_2.collision_radius:
                        character_1.resolve_collision(character_2)                
    
    def apply_entity_collision_updates(self):
        for entity in self.entities:
            entity.apply_collision_updates()

    def kill_dead_entities(self):
        for entity in self.entities:
            if entity.energy <= 0:
                self.entities.remove(entity)
        
    def set_inputs(self, keys_down, key_downs, mouse_pos, mouses_down):
        self.player_inputs.keys_down, self.player_inputs.key_downs, self.player_inputs.mouse_pos, self.player_inputs.mouses_down = keys_down, key_downs, mouse_pos, mouses_down
    
    def get_rendered_screen(self):
        self.camera.get_rendered_screen(self.entities)