'''
Created on Apr 30, 2014

@author: john
'''

import pygame, random
from threading import Thread
from pygame.locals import *
from network import *

from View import View
from Ship import Ship

from Events import Broadcaster

class ClientController():
    def __init__(self):
        self.onShipDeath = Broadcaster()
        self.onBulletDeath = Broadcaster()
    
    def move_ship(self):
        pass
    
    def turn_left(self):
        pass
    
    def turn_right(self):
        pass
    
    def shoot(self):
        pass

class Client(Handler):
    def __init__(self, host, port, view, client_controller):
        Handler.__init__(self, host, port)
        self.view = view
        self.controller = client_controller
    
    def on_close(self):
        pass
    
    def on_msg(self, msg):
        if 'start' in msg:
            for wall in msg['start']:
                self.view.wall_list.append(wall)
        elif 'update' in msg:
            self.view.ship_list = msg['update']['ships']
            self.view.bullet_list = msg['update']['bullets']
            self.view.set_camera_loc(msg['update']['location'])
            for ship_ID in msg['update']['ship_deaths']:
                self.controller.onShipDeath.fire(ship_ID)
            for bullet_ID in msg['update']['bullet_deaths']:
                self.controller.onBulletDeath.fire(bullet_ID[0], bullet_ID[1])                                                                           

map_dimensions = (3200, 1800)

camera_bounds = (854, 480)

controller = ClientController()
view = View(camera_bounds, controller, map_dimensions)
host, port = 'localhost', 8888
client = Client(host, port, view, controller)


def read_input(onMove, onTurnLeft, onTurnRight, onShoot):
    keys = pygame.key.get_pressed()
    if keys[K_w] or keys[K_UP]:
        onMove()
    if keys[K_a] or keys[K_LEFT]:
        onTurnLeft()
    if keys[K_d] or keys[K_RIGHT]:
        onTurnRight()
    if keys[K_SPACE]:
        onShoot()

# view.wall_list = logic.wall_list
# view.bullet_list = logic.bullet_list
# view.ship_list = logic.ship_list

def periodic_poll():
    while 1:
        poll(timeout=0.05)

clock = pygame.time.Clock()
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
#     player_ship.moved = False
    read_input(controller.move_ship, controller.turn_left, controller.turn_right, controller.shoot)
    
    view.draw_everything()