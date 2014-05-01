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

pygame.init()
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
pygame.display.set_caption("VV Pilot")

icon = pygame.Surface((32, 32))
icon.fill(WHITE)
pygame.gfxdraw.polygon(icon, ((3, 29), (29, 29), (16, 3)), BLACK)
pygame.gfxdraw.polygon(icon, ((4, 28), (28, 28), (16, 3)), BLACK)
pygame.gfxdraw.aapolygon(icon, ((2, 30), (30, 30), (15, 2)), BLACK)
pygame.display.set_icon(icon)

display = None

# player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY, respawn_func)

# pygame.draw.polygon(display, RED, [(x-dimx, y+dimy), (x+dimx, y+dimy), (x, y-dimy)], 1)
# pygame.display.update()

def init_display(bounds):
    global display
    display = pygame.display.set_mode(bounds)

def draw_ship(ship, camera):
    if not ship.isDead():
        Display.draw_triangle(display, camera, BLACK, ship.location, ship.bounds, ship.direction, 2)
        if ship.moved:
            Display.draw_triangle_offset(display, camera, RED, (ship.location[0], ship.location[1]+ship.bounds[1]*3/2), (ship.bounds[0]/2, ship.bounds[1]/2), ship.direction-180, ship.location, 2)
            
def draw_bullet(bullet, camera):
    Display.draw_circle(display, camera, BLUE, bullet.location, bullet.bounds[0])
    
def draw_wall(wall, camera):
    Display.draw_rect(display, camera, GREEN, wall, 2)

def draw_everything(ships, bullets, debris, walls, camera):
    display.fill(WHITE)
    for ship in ships:
        draw_ship(ship, camera)
    for bullet in bullets:
        draw_bullet(bullet, camera)
    i = 0
    while i < len(debris):
        debra = debris[i]
        loc = (debra[0][0] + debra[1][0], debra[0][1] + debra[1][1])
        dur = debra[2] - 1
        debris[i] = (loc, debra[1], dur, debra[3], debra[4], debra[5], debra[6], debra[7])
        debra = debris[i]
        Display.draw_circle(display, camera, debra[7], debra[0], int((debra[6]-debra[2])*debra[3]) + debra[4], debra[5])
        if debris[i][2]<=0:
            debris.remove(debris[i])
        else:
            i+=1
    for wall in walls:
        draw_wall(wall, camera)
    pygame.display.update()