'''
Created on Apr 17, 2014

@author: john
'''

import pygame, math

class Ship:
    def __init__(self, location, bounds, shoot_delay, acceleration, max_speed, turn_rate, direction = 0, velocity = (0.0, 0.0)):
        self.location = location
        self.bounds = bounds
        self.shoot_delay = shoot_delay
        self.delay = 0
        self.velocity = velocity
        self.direction = direction
        self.rect = pygame.Rect(location[0]-bounds[0]/2, location[1]-bounds[1]/2, bounds[0]*2, bounds[1]*2)
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.turn_rate = turn_rate
        
    def update(self):
        self.location = (self.location[0] + self.velocity[0], self.location[1] + self.velocity[1])
        self.rect.center = self.location
        if self.delay>0:
            self.delay = self.delay-1
        
    def turn(self, turn_speed):
        self.direction += turn_speed
        
    def turn_left(self):
        self.turn(-self.turn_rate)
        
    def turn_right(self):
        self.turn(self.turn_rate)
        
    def move(self):
        sinD = math.sin(math.radians(self.direction))
        cosD = math.cos(math.radians(self.direction))
        self.velocity = (self.velocity[0] + self.acceleration*sinD, self.velocity[1] - self.acceleration*cosD)
        mag = math.sqrt(math.pow(self.velocity[0], 2) + math.pow(self.velocity[1], 2))
        if mag>self.max_speed:
            self.velocity = (self.velocity[0]/mag*self.max_speed, self.velocity[1]/mag*self.max_speed)
    