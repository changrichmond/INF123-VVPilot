'''
Created on Apr 30, 2014

@author: john
'''

import pygame
from pygame.locals import *

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