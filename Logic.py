'''
Created on Apr 29, 2014

@author: john
'''

import pygame, math, random
from pygame.locals import *
from Ship import Ship
from Bullet import Bullet

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

bulletList = []

wall_list = []

ship_list = []

ship_controllers = []
        

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

# pygame.draw.polygon(display, RED, [(x-dimx, y+dimy), (x+dimx, y+dimy), (x, y-dimy)], 1)
# pygame.display.update()
while True:
    clock.tick(60)
#     x, y = player_ship.location
#     velx, vely = player_ship.velocity
#     dimx, dimy = player_ship.bounds
    moved = False
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    
    for controller in ship_controllers:
        controller()
#     if not player_ship.isDead():
#         sinD = math.sin(math.radians(player_ship.direction))
#         cosD = math.cos(math.radians(player_ship.direction))
#         keys = pygame.key.get_pressed()
#         if keys[K_w] or keys[K_UP]:
#             player_ship.move()
#             moved = True
#         if keys[K_a] or keys[K_LEFT]:
#             player_ship.turn_left()
#         if keys[K_d] or keys[K_RIGHT]:
#             player_ship.turn_right()
#         if keys[K_SPACE] and player_ship.delay<=0:
#             bullet = Bullet((x + dimy*sinD, y-dimy*cosD), (BULLET_SIZE, BULLET_SIZE), player_ship.direction, (BULLET_SPEED*sinD, -BULLET_SPEED*cosD), BULLET_DURATION)
#             #bullet = (x + dimy*sinD, y-dimy*cosD, player_ship.direction, BULLET_DURATION)
#             bulletList.append(bullet)
#             player_ship.delay = SHOOT_DELAY
#             player_ship.move_from_force_in_direction(player_ship.acceleration, player_ship.direction+180)
    
    for ship in ship_list:
        ship.update()
    
    for n in wall_list:
        for ship in ship_list:
            if ship.rect.colliderect(n) and not ship.isDead():
                ship.kill(DEATH_TIME)
    
    
    i = 0
    while i < len(bulletList):
        
        bullet = bulletList[i]
        bullet.update()
        for n in wall_list:
            if n.colliderect(bullet.rect):
                bullet.duration = 0
        if bullet.duration>0:
            i = i+1
        else:
            bulletList.remove(bulletList[i])
    
    pygame.display.update()
