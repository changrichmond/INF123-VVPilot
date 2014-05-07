'''
Created on Apr 30, 2014

@author: john
'''

from Logic import Logic
from Bullet import Bullet
import math

class ServerSideController:
    
    def __init__(self, player_ship, logic, BULLET_SIZE, BULLET_SPEED, BULLET_DURATION, SHOOT_DELAY):
        self.player_ship = player_ship
        self.logic = logic
        self.BULLET_SIZE = BULLET_SIZE
        self.BULLET_SPEED = BULLET_SPEED
        self.BULLET_DURATION = BULLET_DURATION
        self.SHOOT_DELAY = SHOOT_DELAY
        
    def move_ship(self):
        if not self.player_ship.isDead():
            self.player_ship.move()
            self.player_ship.moved = True
    
    def turn_left(self):
        if not self.player_ship.isDead():
            self.player_ship.turn_left()
    
    def turn_right(self):
        if not self.player_ship.isDead():
            self.player_ship.turn_right()
        
    def shoot(self):
        if self.player_ship.delay<= 0 and not self.player_ship.isDead():
            sinD = math.sin(math.radians(self.player_ship.direction))
            cosD = math.cos(math.radians(self.player_ship.direction))
            bullet = Bullet((self.player_ship.location[0] + self.player_ship.bounds[0]*sinD, self.player_ship.location[1]-self.player_ship.bounds[1]*cosD), (self.BULLET_SIZE, self.BULLET_SIZE), self.player_ship.direction, (self.BULLET_SPEED*sinD, -self.BULLET_SPEED*cosD), self.BULLET_DURATION, self.player_ship)
            self.logic.bullet_list.append(bullet)
            self.player_ship.delay = self.SHOOT_DELAY
            self.player_ship.move_from_force_in_direction(self.player_ship.acceleration, self.player_ship.direction+180)