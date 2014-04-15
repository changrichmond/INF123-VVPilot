'''
Created on Apr 2, 2014

@author: Cory
'''
import pygame, math
from pygame.locals import *

pygame.init()
pygame.key.set_repeat(50,50)

RED = (255,0,0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

SPEED = 0.5
BULLET_SPEED = 10
ANGULAR_VELOCITY = 4
VELOCITY_CAP = 5
direction = 0

display = pygame.display.set_mode((1024,768))
location = (320, 240)
velocity = (0, 0)
dimensions = (30, 30)

clock = pygame.time.Clock()

bulletList = []

# pygame.draw.polygon(display, RED, [(x-dimx, y+dimy), (x+dimx, y+dimy), (x, y-dimy)], 1)
# pygame.display.update()
while True:
    clock.tick(60)
    x, y = location
    velx, vely = velocity
    dimx, dimy = dimensions
    display.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        sinD = math.sin(math.radians(direction))
        cosD = math.cos(math.radians(direction))
        keys = pygame.key.get_pressed()
        if keys[K_w] or keys[K_UP]:
            velocity = (velx + SPEED*sinD, vely - SPEED*cosD)
            velx, vely = velocity
            mag = math.sqrt(velx*velx + vely*vely)
            if mag>VELOCITY_CAP:
                velocity = (velx/mag*VELOCITY_CAP, vely/mag*VELOCITY_CAP)
        if keys[K_a] or keys[K_LEFT]:
            direction -= ANGULAR_VELOCITY
        if keys[K_d] or keys[K_RIGHT]:
            direction += ANGULAR_VELOCITY
        if keys[K_SPACE]:
            bullet = (x, y, direction)
            bulletList.append(bullet)
    
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
    
    i = 0
    while i < len(bulletList):
        
        bx, by, bdir = bulletList[i]
        bsinD = math.sin(math.radians(bdir))
        bcosD = math.cos(math.radians(bdir))
        bulletList[i] = (bx + BULLET_SPEED*bsinD, by - BULLET_SPEED*bcosD, bdir)
        pygame.draw.circle(display, BLUE, (int(bx), int(by)), 3)
        i = i+1
    
    pygame.display.update()
