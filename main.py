import pygame as pg, numpy as np
from pygame.locals import *
from random import randint
pg.init()


from settings import Settings
from game import Game
from entities import Circle
from constants import *

game = Game()



dude = Circle(True)

game.add_entity(dude)

keys_down = []
key_downs = []

display = pg.display.set_mode((game.settings.display_width, game.settings.display_height), game.settings.fullscreen)
clock = pg.time.Clock()

running = True
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
        if event.type == pg.KEYUP:
            keys_down.remove(event.key)

    game.set_inputs(keys_down, key_downs, mouse_pos/game.camera.zoom_factor, mouses_down)
    game.tick()
    display.blit(game.get_rendered_screen(), (0,0))
    pg.display.flip()

    clock.tick(game.settings.framerate)


pg.quit()