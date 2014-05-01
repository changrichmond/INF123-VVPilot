'''
Created on Apr 30, 2014

@author: john
'''

import pygame, View, KeyboardInput
from pygame.locals import *

ships = []
bullets = []
debris = []
walls = []

onMove = None
onTurnLeft = None
onTurnRight = None
onShoot = None

def run():
    KeyboardInput.read_input(onMove, onTurnLeft, onTurnRight, onShoot)
    View.draw_everything(ships, bullets, debris, walls)