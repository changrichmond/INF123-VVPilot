'''
Created on Apr 30, 2014

@author: john
'''

import math, pygame, random
from pygame.locals import QUIT

from Bullet import Bullet
from Ship import Ship
from Camera import Camera

class sp_controller:
    def __init__(self, player_ship, bulletList, BULLET_SIZE, BULLET_SPEED, BULLET_DURATION, SHOOT_DELAY):
        self.player_ship = player_ship
        self.bulletList = bulletList
        self.BULLET_SIZE = BULLET_SIZE
        self.BULLET_SPEED = BULLET_SPEED
        self.BULLET_DURATION = BULLET_DURATION
        self.SHOOT_DELAY = SHOOT_DELAY
        self.shoot_timer = 0
        
    def move_ship(self):
        self.player_ship.move()
        self.player_ship.moved = True
    
    def turn_left(self):
        self.player_ship.turn_left()
    
    def turn_right(self):
        self.player_ship.turn_right()
        
    def shoot(self):
        if self.shoot_timer<= 0:
            sinD = math.sin(math.radians(self.player_ship.direction))
            cosD = math.cos(math.radians(self.player_ship.direction))
            bullet = Bullet((self.player_ship.location[0] + self.player_ship.bounds[0]*sinD, self.player_ship.location[1]-self.player_ship.bounds[1]*cosD), (self.BULLET_SIZE, self.BULLET_SIZE), self.player_ship.direction, (self.BULLET_SPEED*sinD, -self.BULLET_SPEED*cosD), self.BULLET_DURATION)
            #bullet = (x + dimy*sinD, y-dimy*cosD, player_ship.direction, BULLET_DURATION)
            self.bulletList.append(bullet)
            self.player_ship.delay = self.SHOOT_DELAY
            self.player_ship.move_from_force_in_direction(self.player_ship.acceleration, self.player_ship.direction+180)
        
    def control(self):
        KeyboardInput.read_input(self.move_ship, self.turn_left, self.turn_right, self.shoot)
        
        
import View, Logic, KeyboardInput

def respawn_func(ship):
    ship.location = (320, 240)
    ship.rect.center = ship.location
    ship.velocity = (0, 0)
    ship.direction = 0

pygame.init()
pygame.key.set_repeat(15,15)

SPEED = 0.075
BULLET_SPEED = 10
BULLET_DURATION = 60
BULLET_SIZE = 5
ANGULAR_VELOCITY = 4
VELOCITY_CAP = 5
SHOOT_DELAY = 10
map_dimensions = (3200, 1800)

#player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY, respawn_func)
DEATH_TIME = 120

start_location = (320, 240)

clock = pygame.time.Clock()

ship_list = []
wall_list = []
bullet_list = []

for i in range(0, 100):
    x = random.randint(start_location[0], 3200)
    y = random.randint(start_location[1], 1800)
    w = random.randint(100, 200)
    h = random.randint(100, 200)
    wall_list.append(pygame.Rect(x, y, w, h))
    
wall_list.append(pygame.Rect(0, 0, map_dimensions[0], 25))
wall_list.append(pygame.Rect(0, 0, 25, map_dimensions[1]))
wall_list.append(pygame.Rect(0, map_dimensions[1]-25, map_dimensions[0], 25))
wall_list.append(pygame.Rect(map_dimensions[0]-25, 0, 25, map_dimensions[1]))

player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY, respawn_func)

controller = sp_controller(player_ship, bullet_list, BULLET_SIZE, BULLET_SPEED, BULLET_DURATION, SHOOT_DELAY)

clock = pygame.time.Clock()
ship_list.append(player_ship)

camera_bounds = (854, 480)
camera_start_location = (320, 240)

# camera = {'location':(320, 240), 'bounds':camera_bounds}
camera = Camera(camera_start_location, camera_bounds)

View.init_display(camera_bounds)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    KeyboardInput.read_input(controller.move_ship, controller.turn_left, controller.turn_right, controller.shoot)
    camera.set_camera_loc(player_ship.location)
    camera.bound_camera(map_dimensions)
    Logic.doLogic(ship_list, bullet_list, wall_list)
    View.draw_everything(ship_list, bullet_list, [], wall_list, camera)
    player_ship.moved = False
            