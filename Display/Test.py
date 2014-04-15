'''
Created on Apr 2, 2014

@author: Cory
'''
import pygame
from pygame.locals import *

pygame.init()
pygame.key.set_repeat(50,50)

RED = (255,0,0)
WHITE = (255, 255, 255)

display = pygame.display.set_mode((640,480))
location = (320, 240)
dimensions = (30, 30)

clock = pygame.time.Clock()

# pygame.draw.polygon(display, RED, [(x-dimx, y+dimy), (x+dimx, y+dimy), (x, y-dimy)], 1)
# pygame.display.update()
while True:
    clock.tick(10)
    x, y = location
    dimx, dimy = dimensions
    display.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == K_w or key == K_UP:
                location = (x, y - 5)
            if key == K_a or key == K_LEFT:
                location = (x - 5, y)
            if key == K_s or key == K_DOWN:
                location = (x, y + 5)
            if key == K_d or key == K_RIGHT:
                location = (x + 5, y)
    
    pygame.draw.polygon(display, RED, [(x-dimx, y+dimy), (x+dimx, y+dimy), (x, y-dimy)], 1)
    
    pygame.display.update()
