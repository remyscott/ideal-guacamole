import pygame as pg, numpy as np
from pygame.locals import *
from random import randint
pg.init()


from game_functions import *
from settings_functions import Settings_functions
Settings_functions.reset_settings()
Settings = Settings_functions.get_settings()

should_be_transparent = (0, 255, 255, 0)
background_color = (200,220,240)




class Circle():
    def __init__(self):
        #By default dependent on size
        self.size = 1
        self.acceleration_ps = self.size*60
        self.max_energy = 5*self.size
        self.acceleration_per_energy = 20*60
        self.battery_charge_per_second = self.size
        self.energy_per_fuel = 500
        self.max_fuel = self.size*.2
        self.mass = self.size**2
        self.camera_offset = np.array((-self.size, -self.size))
        

        #Basic non-attributes
        self.pos = np.array([randint(0,30),randint(0,15)],np.float64)
        self.vel = np.array([1,0],np.float64)
        self.ability_charge = 0
        self.energy = 1
        self.ability_cooldown_left = 0
        self.fuel_left = self.max_fuel

        #charictaristics
        self.fueltype = 'plutonium'
        self.rendertype = 'circle'
        self.movementtype = '4_thruster'
        self.color = (0,0,0)
        
        #stats
        self.max_ability_cooldown = 1
        self.sheild_momentum_per_energy = 100
        self.ability_charge_time = 1
        self.health = 1
        self.ability_factor = 60

        #behavior
        self.safety = self.max_energy/5

        #for collison
        self.collision_movement_needed = np.array([0,0], np.float64)


    def actions(self, keys_down, key_downs, mouse_pos, mouses_down):
        for key in keys_down:
            if self.energy >= self.safety:
                if key == K_d:
                    self.accelerate([1,0])
                if key == K_q:
                    self.health -= .1
                if key == K_w:
                    self.accelerate([0,-1])
                if key == K_a:
                    self.accelerate([-1,0])
                if key == K_s:
                    self.accelerate([0,1])
        
        if mouses_down[2]:
            if self.ability_cooldown_left <= 0 and self.energy > self.safety:
                self.ability_charge += 1/(Settings.FRAMERATE*self.ability_charge_time)
                self.energy -= 1/(Settings.FRAMERATE*self.ability_charge_time)
        
        
        elif self.ability_charge > 0:
            self.dash()
        
    def update(self, actions, keys_down, key_downs, mouse_pos, mouses_down):
        if self.ability_cooldown_left > 0:
            self.ability_cooldown_left -= 1/Settings.FRAMERATE
        if self.energy < self.max_energy - self.battery_charge_per_second/Settings.FRAMERATE and self.fuel_left > 0:
            self.energy += self.battery_charge_per_second/Settings.FRAMERATE
            self.fuel_left -= (self.battery_charge_per_second/Settings.FRAMERATE)/self.energy_per_fuel
        
        if actions:
            self.actions(keys_down, key_downs, mouse_pos, mouses_down)

        self.ability_charge -= (self.ability_charge/10)**2




        self.vel -= self.vel/(self.size*.54)/Settings.FRAMERATE
        self.pos += self.vel/Settings.FRAMERATE

    def accelerate(self, vector):
        self.vel += self.acceleration_ps * np.array(vector) / ((self.size**2) * Settings.FRAMERATE)
        self.energy -= np.sqrt(vector[0]**2+vector[1]**2)/self.acceleration_per_energy

    def dash(self):
        dash_energy = self.ability_charge * self.ability_factor
        velocity_change =  dash_energy / self.size**2
        dash_vector = (mouse_pos/Settings.CAMERA_ZOOM_FACTOR-self.pos+[-self.size,-self.size])/Settings.CAMERA_ZOOM_FACTOR
        self.vel += normalize(dash_vector) * velocity_change
        
        self.ability_charge = 0
        self.ability_cooldown_left = self.max_ability_cooldown

    def handle_collision(self, object):
        self_mass_to_total_mass = self.mass/(self.mass+object.mass)
        vector_to_object = self.pos - object.pos
        normalized_vector = normalize(vector)

        distance_needed = character_1.size + character_2.size - distance
        vector_needed = normalized_vector * distance_needed * (1-c1_to_whole)
        collision_energy = (distance_needed*c1_to_whole*c1_mass + distance_needed*(1-c1_to_whole)*c2_mass)*Settings.FRAMERATE
                    
        character_1.collision_movement_needed += vector_needed
        character_1.vel += 2*vector_needed
        character_1.energy -= collision_energy/character_1.sheild_momentum_per_energy


    def get_render(self, camera_zoom_factor):
        
        hull_render = self.render_hull(camera_zoom_factor)
        energy_render = self.render_battery(camera_zoom_factor)
        fuel_render, fuel_render_offset_vector = self.render_fuel(camera_zoom_factor)
        ability_render = self.render_ability(camera_zoom_factor)
        
        rect = hull_render.get_rect()

        hull_render.blit(fuel_render, (np.array(rect.center)+fuel_render_offset_vector/2))
        hull_render.blit(ability_render, (rect.centerx, 0))                                                    
        hull_render.blit(energy_render, (0,0))
        
        return(hull_render)
    
    def render_hull(self, camera_zoom_factor):

        radius_pixels = self.size*camera_zoom_factor
    
        rendered_hull = pg.surface.Surface((radius_pixels*2, radius_pixels*2)).convert_alpha()
        rendered_hull.fill(should_be_transparent)
        pg.draw.circle(rendered_hull, self.color,rendered_hull.get_rect().center, radius_pixels, 0)

        return(rendered_hull)

    def render_fuel(self, camera_zoom_factor):

        fuel_radius_pixels = self.size*(self.max_fuel/self.size) *camera_zoom_factor
        fuel_render = pg.surface.Surface((fuel_radius_pixels*2, fuel_radius_pixels*2)).convert_alpha()   
        fuel_render.fill(should_be_transparent)

        pg.draw.circle(fuel_render, (200,200,255,255),fuel_render.get_rect().center,fuel_radius_pixels,0)

        rect = fuel_render.get_rect()
        fuel_render_offset_vector = -np.array(rect.size)
        #for x in range(0,rect.size[0]):
            #for y in range(0,rect.size[1]):
                #if randint(0,101)/100 > c.fuel_left/c.max_fuel:
                #    fuel_render.set_at((x,y),(0,0,0,0))
        return(fuel_render, fuel_render_offset_vector)
        
    def render_battery(self, camera_zoom_factor): #character, diameter
        battery_surface_size_pixels = self.size * camera_zoom_factor
        battery_radius_pixels = self.size*(self.energy/self.max_energy) *camera_zoom_factor
        energy_render = pg.surface.Surface((battery_surface_size_pixels, battery_surface_size_pixels)).convert_alpha()   
        energy_render.fill(should_be_transparent)
        pg.draw.circle(energy_render, (100,100,255,255), (battery_surface_size_pixels,battery_surface_size_pixels), battery_radius_pixels,0)
        return(energy_render)
    
    def render_ability(self, camera_zoom_factor):
        ability_radius_pixels = self.size*camera_zoom_factor
        ability_render = pg.surface.Surface((ability_radius_pixels, ability_radius_pixels)).convert_alpha()   
        ability_render.fill(should_be_transparent)

        if self.ability_cooldown_left > 0:
            pg.draw.circle(ability_render, (255,0,0, min((self.ability_cooldown_left/self.max_ability_cooldown)*255,255)) ,(0,ability_radius_pixels),ability_radius_pixels,0)

        elif self.ability_charge > 0:
            pg.draw.circle(ability_render, self.get_ability_charge_color(), (0,ability_radius_pixels), ability_radius_pixels,0)

        return(ability_render)

        
    def get_ability_charge_color(self):
        color = (255,0,255)
        if self.ability_charge <= 1:
            color = (255,255,255,min(self.ability_charge*255,255))
        if self.ability_charge > 1 and self.ability_charge <= 6 :
            color = (max(255-(self.ability_charge-1)*51, 0),max(255-(self.ability_charge-1)*51, 0),255,255)
        return(color)

    

class Camera():
    def __init__(self, position):
        self.zoom_factor = 40
        self.pos = np.array(position, np.float64)
        self.screen = pg.surface.Surface((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        
    def render_screen(self, characters):
        self.screen.fill(background_color)
        
        for character in characters:
            character_render = character.get_render(self.zoom_factor)
            self.screen.blit(character_render, self.pos_to_screenspace(character.pos, character.camera_offset))
        
        return(self.screen)
    def pos_to_screenspace(self, position, offset):
        camera_relative_position = (position+offset - self.pos) * self.zoom_factor
        return(camera_relative_position)

    def get_screen(self):
        return(self.screen)

display = pg.display.set_mode((Settings.DISPLAY_WIDTH, Settings.DISPLAY_HEIGHT), Settings.FULLSCREEN)
clock = pg.time.Clock()
default_camera = Camera(position = (0,0))
running = True


sword_dude_0 = Circle()

player_controlled = [sword_dude_0]
all_characters = [sword_dude_0]

keys_down = []
key_downs = []

while running:
    events = pg.event.get()
    mouse_pos = np.array(pg.mouse.get_pos())
    mouses_down = list(pg.mouse.get_pressed())
    key_downs = []
    for event in events:
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            keys_down.append(event.key)
            key_downs.append(event.key)
            if event.key == K_e:
                new_thing = Circle()
                player_controlled.append(new_thing)
                all_characters.append(new_thing)

        if event.type == pg.KEYUP:
            keys_down.remove(event.key)

    
    
    
    for character in player_controlled:
        character.update(True,keys_down, key_downs, mouse_pos, mouses_down)

    for character in all_characters:
        if character not in player_controlled:
            character.update(False,keys_down, key_downs, mouse_pos, mouses_down)
    
    for character_1 in all_characters:
        for character_2 in all_characters:
            if not character_1 == character_2:
                # + character_2.vel/Settings.FRAMERATE
                vector = (character_1.pos) - (character_2.pos)
                distance = length(vector)

                if distance <= character_1.size + character_2.size:
                    character_1.resolve_collision(character_2)
                    
                    


    
    for character in all_characters:
        if character.energy <= 0:
            all_characters.remove(character)
    
    for character in all_characters:
        character.pos += character.collision_movement_needed*1
        character.collision_movement_needed *= 0

    display.blit(default_camera.render_screen(all_characters), (0,0))

    pg.display.flip()
    clock.tick(Settings.FRAMERATE)


pg.quit()