'''
Created on Apr 2, 2014

@author: Cory
'''
import pygame, math, random
from pygame.locals import *
import Display

pygame.init()
pygame.key.set_repeat(15,15)

RED = (255,0,0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SPEED = 0.1
BULLET_SPEED = 10
BULLET_DURATION = 60
BULLET_SIZE = 5
ANGULAR_VELOCITY = 2
VELOCITY_CAP = 5
SHOOT_DELAY = 10
map_dimensions = (3200, 1800)
camera_bounds = (854, 480)

camera = {'location':(320, 240), 'bounds':camera_bounds}

display = pygame.display.set_mode(camera_bounds)
location = (320, 240)
velocity = (0, 0)
dimensions = (15, 15)
ship_rect = pygame.Rect(location[0] - dimensions[0]/2, location[1]-dimensions[1]/2, dimensions[0], dimensions[1])
direction = 0
delay = 0

clock = pygame.time.Clock()

bulletList = []

wall_list = []

for i in range(0, 100):
    x = random.randint(0, 3200)
    y = random.randint(0, 1800)
    w = random.randint(100, 200)
    h = random.randint(100, 200)
    wall_list.append(pygame.Rect(x, y, w, h))

# pygame.draw.polygon(display, RED, [(x-dimx, y+dimy), (x+dimx, y+dimy), (x, y-dimy)], 1)
# pygame.display.update()
while True:
    clock.tick(60)
    if delay>0:
        delay = delay-1
    x, y = location
    velx, vely = velocity
    dimx, dimy = dimensions
    display.fill(WHITE)
    moved = False
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
    sinD = math.sin(math.radians(direction))
    cosD = math.cos(math.radians(direction))
    keys = pygame.key.get_pressed()
    if keys[K_w] or keys[K_UP]:
        velocity = (velx + SPEED*sinD, vely - SPEED*cosD)
        velx, vely = velocity
        mag = math.sqrt(velx*velx + vely*vely)
        if mag>VELOCITY_CAP:
            velocity = (velx/mag*VELOCITY_CAP, vely/mag*VELOCITY_CAP)
        moved = True
    if keys[K_a] or keys[K_LEFT]:
        direction -= ANGULAR_VELOCITY
    if keys[K_d] or keys[K_RIGHT]:
        direction += ANGULAR_VELOCITY
    if keys[K_SPACE] and delay<=0:
        bullet = (x + dimy*sinD, y-dimy*cosD, direction, BULLET_DURATION)
        bulletList.append(bullet)
        delay = SHOOT_DELAY
        velocity = (velx - SPEED*sinD, vely + SPEED*cosD)
        velx, vely = velocity
        mag = math.sqrt(velx*velx + vely*vely)
        if mag>VELOCITY_CAP:
            velocity = (velx/mag*VELOCITY_CAP, vely/mag*VELOCITY_CAP)
    
    location = (x+velx, y+vely)
    x, y = location
    ship_rect = pygame.Rect(x-dimx, y-dimy, dimx*2, dimy*2)
    
    for n in wall_list:
        if ship_rect.colliderect(n):
            print "colliding"
    
    Display.set_camera_loc(camera, (x, y))
    Display.bound_camera(camera, map_dimensions)
        
    sinD = math.sin(math.radians(direction))
    cosD = math.cos(math.radians(direction))
    Display.draw_triangle(display, camera, BLACK, location, dimensions, direction, 2)
    if moved:
        Display.draw_triangle_offset(display, camera, RED, (location[0], location[1]+dimensions[1]*3/2), (dimensions[0]/2, dimensions[1]/2), direction-180, location, 2)
    
    i = 0
    while i < len(bulletList):
        
        bx, by, bdir, bdur = bulletList[i]
        bsinD = math.sin(math.radians(bdir))
        bcosD = math.cos(math.radians(bdir))
        bdur = bdur - 1
        bulletList[i] = (bx + BULLET_SPEED*bsinD, by - BULLET_SPEED*bcosD, bdir, bdur)
        Display.draw_circle(display, camera, BLUE, (bx, by), BULLET_SIZE)
        if bdur <= 0:
            bulletList.remove(bulletList[i])
        else:
            i = i+1
    for n in wall_list:
        Display.draw_rect(display, camera, GREEN, n, 2)
    
    pygame.display.update()
