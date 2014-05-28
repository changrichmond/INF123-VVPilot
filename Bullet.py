'''
Created on Apr 24, 2014

@author: Cory
'''

import pygame

class Bullet:
    CUR_ID = 0
    def __init__(self, location, bounds, direction, velocity, duration = 0, ship = None):
        self.location = location
        self.bounds = bounds
        self.direction = direction
        self.velocity = velocity
        self.duration = duration
        self.ship = ship
        self.rect = pygame.Rect(location[0]-bounds[0], location[1]-bounds[1], bounds[0]*2, bounds[1]*2)
        self.id = Bullet.CUR_ID
        Bullet.CUR_ID+=1
        
    def update(self):
        self.duration -= 1
        self.location = (self.location[0] + self.velocity[0], self.location[1] + self.velocity[1])
        self.rect.center = self.location
        
    def is_dead(self):
        return self.duration <= 0