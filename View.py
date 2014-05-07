'''
Created on Apr 30, 2014

@author: john
'''

import pygame, math, random
import pygame.gfxdraw
from pygame.locals import *
import Display
from Ship import Ship
from Camera import Camera
from Bullet import Bullet
# pygame.key.set_repeat(15,15)

RED = (255,0,0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# SPEED = 0.075
# BULLET_SPEED = 10
# BULLET_DURATION = 60
# BULLET_SIZE = 5
# ANGULAR_VELOCITY = 4
# VELOCITY_CAP = 5
# SHOOT_DELAY = 10
# map_dimensions = (3200, 1800)

#we legit now son

# player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY, respawn_func)

# pygame.draw.polygon(display, RED, [(x-dimx, y+dimy), (x+dimx, y+dimy), (x, y-dimy)], 1)
# pygame.display.update()

class View:
    
    def __init__(self, camera_bounds, event_system, world_bounds):
        pygame.init()
        self.display = pygame.display.set_mode(camera_bounds)
        pygame.display.set_caption("VV Pilot")

        icon = pygame.Surface((32, 32))
        icon.fill(WHITE)
        pygame.gfxdraw.polygon(icon, ((3, 29), (29, 29), (16, 3)), BLACK)
        pygame.gfxdraw.polygon(icon, ((4, 28), (28, 28), (16, 3)), BLACK)
        pygame.gfxdraw.aapolygon(icon, ((2, 30), (30, 30), (15, 2)), BLACK)
        pygame.display.set_icon(icon)
        # initialize the lists
        self.ship_list = []
        self.bullet_list = []
        self.wall_list = []
        self.debris = []
        # make the camera
        self.camera = Camera((camera_bounds[0]/2, camera_bounds[1]/2), camera_bounds)
        self.world_bounds = world_bounds
        # add the view to the event system
        event_system.onShipDeath+=self.onShipDeath
        event_system.onBulletDeath+=self.onBulletDeath
        
    def onShipDeath(self, ship):
        Display.death_animation(ship, self.debris, BLACK)
        
    def onBulletDeath(self, bullet, wall_rect):
        Display.bullet_death(bullet, wall_rect, self.debris, BLUE)
        
    def draw_ship(self, ship):
        if not ship.isDead():
            Display.draw_triangle(self.display, self.camera, BLACK, ship.location, ship.bounds, ship.direction, 2)
            if ship.moved:
                Display.draw_triangle_offset(self.display, self.camera, RED, (ship.location[0], ship.location[1]+ship.bounds[1]*3/2), (ship.bounds[0]/2, ship.bounds[1]/2), ship.direction-180, ship.location, 2)
                
    def draw_bullet(self, bullet):
        Display.draw_circle(self.display, self.camera, BLUE, bullet.location, bullet.bounds[0])
        
    def draw_wall(self, wall):
        Display.draw_rect(self.display, self.camera, GREEN, wall, 2)
        
    def set_camera_loc(self, location):
        self.camera.set_camera_loc(location)
        self.camera.bound_camera(self.world_bounds)
        
    def draw_everything(self):
        self.display.fill(WHITE)
        for ship in self.ship_list:
            self.draw_ship(ship)
        for bullet in self.bullet_list:
            self.draw_bullet(bullet)
        i = 0
        while i < len(self.debris):
            debra = self.debris[i]
            loc = (debra[0][0] + debra[1][0], debra[0][1] + debra[1][1])
            dur = debra[2] - 1
            self.debris[i] = (loc, debra[1], dur, debra[3], debra[4], debra[5], debra[6], debra[7])
            debra = self.debris[i]
            Display.draw_circle(self.display, self.camera, debra[7], debra[0], int((debra[6]-debra[2])*debra[3]) + debra[4], debra[5])
            if self.debris[i][2]<=0:
                self.debris.remove(self.debris[i])
            else:
                i+=1
        for wall in self.wall_list:
            self.draw_wall(wall)
        pygame.display.update()