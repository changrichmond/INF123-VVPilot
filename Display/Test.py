'''
Created on Apr 2, 2014

@author: Cory
'''
import pygame, math
from pygame.locals import *

pygame.init()
pygame.key.set_repeat(50,50)

RED = (255,0,0)
WHITE = (255, 255, 255)

SPEED = 0.5
ANGULAR_VELOCITY = 5
VELOCITY_CAP = 5
direction = 0

display = pygame.display.set_mode((1024,768))
location = (320, 240)
velocity = (0, 0)
dimensions = (30, 30)

clock = pygame.time.Clock()

# pygame.draw.polygon(display, RED, [(x-dimx, y+dimy), (x+dimx, y+dimy), (x, y-dimy)], 1)
# pygame.display.update()
while True:
    clock.tick(30)
    x, y = location
    velx, vely = velocity
    dimx, dimy = dimensions
    display.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        sinD = math.sin(math.radians(direction))
        cosD = math.cos(math.radians(direction))
        if event.type == KEYDOWN:
            key = event.key
            if key == K_w or key == K_UP:
                velocity = (velx + SPEED*sinD, vely - SPEED*cosD)
                velx, vely = velocity
                mag = math.sqrt(velx*velx + vely*vely)
                if mag>VELOCITY_CAP:
                    velocity = (velx/mag*VELOCITY_CAP, vely/mag*VELOCITY_CAP)
            if key == K_a or key == K_LEFT:
                direction -= ANGULAR_VELOCITY
            if key == K_d or key == K_RIGHT:
                direction += ANGULAR_VELOCITY
    
    location = (x+velx, y+vely)
    sinD = math.sin(math.radians(direction))
    cosD = math.cos(math.radians(direction))
    x1 = -dimx*cosD - dimy*sinD
    y1 = -dimx*sinD + dimy*cosD
    x2 = dimx*cosD - dimy*sinD
    y2 = dimx*sinD + dimy*cosD
    x3 = dimy*sinD
    y3 = -dimy*cosD
    pygame.draw.polygon(display, RED, [(x+x1, y+y1), (x+x2, y+y2), (x+x3, y+y3)], 1)
    
    pygame.display.update()
