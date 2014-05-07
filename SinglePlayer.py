'''
Created on Apr 30, 2014

@author: john
'''

import pygame, random
from pygame.locals import *

from Logic import Logic
from View import View
from Ship import Ship
from ServerSideController import ServerSideController

def respawn_func(ship):
    ship.location = (320, 240)
    ship.rect.center = ship.location
    ship.velocity = (0, 0)
    ship.direction = 0
    
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

SPEED = 0.075
BULLET_SPEED = 10
BULLET_DURATION = 60
BULLET_SIZE = 5
ANGULAR_VELOCITY = 4
VELOCITY_CAP = 5
SHOOT_DELAY = 10
map_dimensions = (3200, 1800)

camera_bounds = (854, 480)

logic = Logic()
view = View(camera_bounds, logic, map_dimensions)

player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY, respawn_func)
logic.ship_list.append(player_ship)

controller = ServerSideController(player_ship, logic, BULLET_SIZE, BULLET_SPEED, BULLET_DURATION, SHOOT_DELAY)

for i in range(0, 100):
    x = random.randint(player_ship.location[0], 3200)
    y = random.randint(player_ship.location[1], 1800)
    w = random.randint(100, 200)
    h = random.randint(100, 200)
    logic.wall_list.append(pygame.Rect(x, y, w, h))
    
logic.wall_list.append(pygame.Rect(0, 0, map_dimensions[0], 25))
logic.wall_list.append(pygame.Rect(0, 0, 25, map_dimensions[1]))
logic.wall_list.append(pygame.Rect(0, map_dimensions[1]-25, map_dimensions[0], 25))
logic.wall_list.append(pygame.Rect(map_dimensions[0]-25, 0, 25, map_dimensions[1]))

view.wall_list = logic.wall_list
view.bullet_list = logic.bullet_list
view.ship_list = logic.ship_list

clock = pygame.time.Clock()

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    player_ship.moved = False
    read_input(controller.move_ship, controller.turn_left, controller.turn_right, controller.shoot)
    logic.doLogic()
    view.set_camera_loc(player_ship.location)
    view.draw_everything()