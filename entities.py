from numpy import array, float64
from pygame.locals import K_d, K_a, K_s, K_w 
from random import randint

class Circle():
    def __init__(self, player_controlled: bool = False):
        #By default dependent on size
        self.size = 1
        self.acceleration_ps = self.size*60
        self.max_energy = 5*self.size
        self.acceleration_per_energy = 20*60
        self.battery_charge_per_second = self.size
        self.energy_per_fuel = 500
        self.max_fuel = self.size*.2
        self.mass = self.size**2
        self.camera_offset = array((-self.size, -self.size))
        

        #Basic non-attributes
        self.player_controlled = player_controlled
        self.pos = array([randint(0,30),randint(0,15)],np.float64)
        self.vel = array([1,0],float64)
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
        self.ability_factor = 60

        #behavior
        self.safety = self.max_energy/5

        #for collison
        self.collision_movement_needed = array([0,0], float64)


    def actions(self, inputs):
        for key in keys_down:
            if self.energy >= self.safety:
                if key == K_d:
                    self.accelerate([1,0])
                if key == K_w:
                    self.accelerate([0,-1])
                if key == K_a:
                    self.accelerate([-1,0])
                if key == K_s:
                    self.accelerate([0,1])
        
        if inputs.mouses_down[2]:
            if self.ability_cooldown_left <= 0 and self.energy > self.safety:
                self.ability_charge += 1/(game.settings.framerate*self.ability_charge_time)
                self.energy -= 1/(game.settings.framerate*self.ability_charge_time)
        
        
        elif self.ability_charge > 0:
            self.dash()
        
    def update(self, inputs):
        if self.ability_cooldown_left > 0:
            self.ability_cooldown_left -= 1/game.settings.framerate
        if self.energy < self.max_energy and self.fuel_left > 0:
            self.energy += self.battery_charge_per_second/game.settings.framerate
            self.fuel_left -= (self.battery_charge_per_second/game.settings.framerate)/self.energy_per_fuel
        
        if self.player_controlled:
            self.actions(inputs)

        self.ability_charge -= (self.ability_charge/10)**2




        self.vel -= self.vel/(self.size*.54)/game.settings.framerate
        self.pos += self.vel/game.settings.framerate

    def accelerate(self, vector):
        self.vel += self.acceleration_ps * np.array(vector) / ((self.size**2) * game.settings.framerate)
        self.energy -= np.sqrt(vector[0]**2+vector[1]**2)/self.acceleration_per_energy

    def dash(self):
        dash_energy = self.ability_charge * self.ability_factor
        velocity_change =  dash_energy / self.size**2
        dash_vector = mouse_pos/game.settings.CAMERA_ZOOM_FACTOR-self.pos+[-self.size,-self.size]
        self.vel += normalize(dash_vector) * velocity_change
        
        self.ability_charge = 0
        self.ability_cooldown_left = self.max_ability_cooldown

    def handle_collision(self, object):
        self_mass_to_total_mass = self.mass/(self.mass+object.mass)
        vector_to_object = self.pos - object.pos
        normalized_vector = normalize(vector)

        distance_needed = character_1.size + character_2.size - distance
        vector_needed = normalized_vector * distance_needed * (1-c1_to_whole)
        collision_energy = (distance_needed*c1_to_whole*c1_mass + distance_needed*(1-c1_to_whole)*c2_mass)*game.settings.framerate
                    
        character_1.collision_movement_needed += vector_needed
        character_1.vel += 2*vector_needed
        character_1.energy -= collision_energy/character_1.sheild_momentum_per_energy

    def apply_collision_updates(self):
        self.pos += self.collision_movement_needed

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
        for x in range(0,rect.size[0]):
            for y in range(0,rect.size[1]):
                if randint(0,101)/100 > self.fuel_left/self.max_fuel:
                    fuel_render.set_at((x,y),(0,0,0,0))
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