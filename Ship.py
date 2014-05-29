'''
Created on Apr 17, 2014

@author: john
'''

import pygame, math
from Events import Broadcaster

def default_respawn(ship):
    ship.location = (0, 0)
    ship.rect.center = ship.location
    ship.velocity = (0, 0)
    ship.direction = 0

class Ship:
    CUR_ID = 0
    def __init__(self, location, bounds, shoot_delay, acceleration, max_speed, turn_rate, respawn_func = default_respawn, direction = 0, velocity = (0.0, 0.0), shield_duration = 120, curr_acceleration = (0.0, 0.0)):
        self.location = location
        self.bounds = bounds
        self.shoot_delay = shoot_delay
        self.delay = 0
        self.velocity = velocity
        self.direction = direction
        self.rect = pygame.Rect(location[0]-bounds[0], location[1]-bounds[1], bounds[0]*2, bounds[1]*2)
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.turn_rate = turn_rate
        self.death_timer = 0
        self.respawn_func = respawn_func
        self.respawn_event = Broadcaster()
        self.moved = False
        self.shield_duration = self.shield = shield_duration*2
        self.shield_obj = None
        self.curr_acceleration = curr_acceleration
        self.id = Ship.CUR_ID
        Ship.CUR_ID+=1
    def update(self):
        #self.velocity = (self.velocity[0] + self.curr_acceleration[0], self.velocity[1] + self.curr_acceleration[1])
        self.location = (self.location[0] + self.velocity[0], self.location[1] + self.velocity[1])
        self.rect.center = self.location
        if self.delay>0:
            self.delay = self.delay-1
        if self.shield < self.shield_duration and not self.shield_obj:
            self.shield+=1
        if self.shield_obj:
            self.shield-=2
            if self.shield<=0:
                self.shield_obj = None
        if self.isDead():
            self.death_timer -= 1
            if not self.isDead():
                self.respawn_func(self)
                self.respawn_event.fire(self)
        
    def turn(self, turn_speed):
        self.direction += turn_speed
        
    def turn_left(self):
        self.turn(-self.turn_rate)
        
    def turn_right(self):
        self.turn(self.turn_rate)
        
    def move(self):
        self.move_from_force_in_direction(self.acceleration, self.direction)
            
    def move_from_force(self, acceleration):
        self.move_from_force_in_direction(acceleration, self.direction)
            
    def move_from_force_in_direction(self, acceleration, direction):
        sinD = math.sin(math.radians(direction))
        cosD = math.cos(math.radians(direction))
        self.velocity = (self.velocity[0] + acceleration*sinD, self.velocity[1] - acceleration*cosD)
        mag = math.sqrt(math.pow(self.velocity[0], 2) + math.pow(self.velocity[1], 2))
        if mag>self.max_speed:
            self.velocity = (self.velocity[0]/mag*self.max_speed, self.velocity[1]/mag*self.max_speed)
            
    def accelerate(self):
        sinD = math.sin(math.radians(self.direction))
        cosD = math.cos(math.radians(self.direction))
        self.curr_acceleration = (self.acceleration*sinD, self.acceleration*cosD)
        
    def reset_acceleration(self):
        self.curr_acceleration = (0.0, 0.0)
            
    def kill(self, death_time):
        self.death_timer = death_time
        self.velocity = (0, 0)
        
    def isDead(self):
        return self.death_timer > 0
    
    def can_toggle_shield(self, flag):
        return not flag or self.shield>self.shield_duration/8
    
    def toggle_shield(self, flag):
        self.is_shielded = flag
    