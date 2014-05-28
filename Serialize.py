'''
Created on May 7, 2014

@author: john
'''

from Ship import Ship
from Bullet import Bullet
import pygame

def serializeObject(obj):
    ans = {}
    for a in dir(obj):
        if not a.startswith('__') and not callable(getattr(obj, a)):
            ans[a] = getattr(obj, a)
    return ans

def serializeShip(ship):
    return { 'location':ship.location, 'bounds':ship.bounds, 
           'direction':ship.direction, 'death_timer':ship.death_timer,
           'moved':ship.moved, 'shield_obj':serializeRect(ship.shield_obj),
           'velocity': ship.velocity, 'id' : ship.id}
    
def deserializeShip(ship):
    retship = Ship(ship['location'], ship['bounds'], 0, 0, 0, 0)
    retship.direction = ship['direction']
    retship.death_timer = ship['death_timer']
    retship.moved = ship['moved']
    retship.shield_obj = deserializeRect(ship['shield_obj'])
    retship.velocity = ship['velocity']
    retship.id = ship['id']
    return retship
    
def serializeBullet(bullet):
    return {'location':bullet.location, 'bounds':bullet.bounds,
            'direction':bullet.direction, 'velocity':bullet.velocity,
            'id' : bullet.id}
    
def deserializeBullet(bullet):
    retbullet = Bullet(bullet['location'], bullet['bounds'], bullet['direction'], bullet['velocity'])
    retbullet.id = bullet['id']
    return retbullet

def serializeRect(rect):
    if not rect:
        return None
    return [rect.x, rect.y, rect.w, rect.h]

def deserializeRect(rect):
    if not rect:
        return None
    return pygame.Rect(rect[0], rect[1], rect[2], rect[3])