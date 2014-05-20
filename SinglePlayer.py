'''
Created on Apr 30, 2014

@author: john
'''

import pygame, random, math
from pygame.locals import *

from Logic import Logic
from View import View
from Ship import Ship
from ServerSideController import ServerSideController
from Bullet import Bullet

def respawn_func(ship):
    ship.location = (320, 240)
    ship.rect.center = ship.location
    ship.velocity = (0, 0)
    ship.direction = 0
    
def random_respawn(minLoc, maxLoc):
    def respawn(ship):
        ship.location = (random.randint(minLoc[0], maxLoc[0]), random.randint(minLoc[1], maxLoc[1]))
        ship.rect.center = ship.location
        ship.velocity = (0, 0)
        ship.direction = 0
    return respawn
    
def read_input(onMove, onTurnLeft, onTurnRight, onShoot, onShield):
    keys = pygame.key.get_pressed()
    if keys[K_w] or keys[K_UP]:
        onMove()
    if keys[K_a] or keys[K_LEFT]:
        onTurnLeft()
    if keys[K_d] or keys[K_RIGHT]:
        onTurnRight()
    if keys[K_SPACE]:
        onShoot()
    if keys[K_s]:
        onShield()
    

SPEED = 0.075
BULLET_SPEED = 10
BULLET_DURATION = 60
BULLET_SIZE = 5
ANGULAR_VELOCITY = 4
VELOCITY_CAP = 5
SHOOT_DELAY = 10
SHIELD_SIZE = 20
NUM_BOTS = 10
NUM_WALLS = 20
map_dimensions = (3200, 1800)

camera_bounds = (854, 480)

logic = Logic()
view = View(camera_bounds, logic, map_dimensions)

min_respawn = (320, 240)
max_respawn = (3000, 1600)

respawn = random_respawn(min_respawn, max_respawn)

player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY, respawn)
logic.add_ship(player_ship)

controller = ServerSideController(player_ship, logic, BULLET_SIZE, BULLET_SPEED, BULLET_DURATION, SHOOT_DELAY, SHIELD_SIZE)

def run_bot_func(bot):
    def on_run():
        if not bot.isDead():
            rng = random.randint(0, 30)
            if rng < 10:
                bot.turn_left()
            elif rng < 20:
                bot.turn_right()
            elif rng < 25:
                bot.move()
            else:
                if bot.delay <= 0:
                    sinD = math.sin(math.radians(bot.direction))
                    cosD = math.cos(math.radians(bot.direction))
                    bullet = Bullet((bot.location[0] + bot.bounds[0]*sinD, bot.location[1]-bot.bounds[1]*cosD), (BULLET_SIZE, BULLET_SIZE), bot.direction, (BULLET_SPEED*sinD, -BULLET_SPEED*cosD), BULLET_DURATION, bot)
                    logic.bullet_list.append(bullet)
                    bot.delay = SHOOT_DELAY
                    bot.move_from_force_in_direction(bot.acceleration, bot.direction+180)
    return on_run

botControllers = []

for i  in range(0, NUM_BOTS):
    ship = Ship((random.randint(min_respawn[0], max_respawn[0]), random.randint(min_respawn[1], max_respawn[1])), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY, respawn)
    logic.add_ship(ship)
    botControllers.append(run_bot_func(ship))

for i in range(0, NUM_WALLS):
    x = random.randint(player_ship.location[0], 3200-player_ship.location[0])
    y = random.randint(player_ship.location[1], 1800-player_ship.location[1])
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
    logic.doLogic()
    read_input(controller.move_ship, controller.turn_left, controller.turn_right, controller.shoot, controller.shield_on)
    for bot in botControllers:
        bot()
    view.set_camera_loc(player_ship.location)
    view.draw_everything()