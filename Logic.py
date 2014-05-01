'''
Created on Apr 29, 2014

@author: john
'''

import pygame, math, random
from pygame.locals import *
from Ship import Ship
from Bullet import Bullet
from Camera import Camera



bulletList = []

wall_list = []

ship_list = []

ship_controllers = []

DEATH_TIME = 120

camera_bounds = (854, 480)
camera_start_location = (320, 240)

# camera = {'location':(320, 240), 'bounds':camera_bounds}
camera = Camera(camera_start_location, camera_bounds)

# pygame.draw.polygon(display, RED, [(x-dimx, y+dimy), (x+dimx, y+dimy), (x, y-dimy)], 1)
# pygame.display.update()

def doLogic(ship_list, bullet_list, wall_list):
#     x, y = player_ship.location
#     velx, vely = player_ship.velocity
#     dimx, dimy = player_ship.bounds
    
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
