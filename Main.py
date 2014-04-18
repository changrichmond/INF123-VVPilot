'''
Created on Apr 2, 2014

@author: Cory
'''
import pygame, math, random
from pygame.locals import *
import Display
from Ship import Ship

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

player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY)
DEATH_TIME = 120
death_timer = 0

clock = pygame.time.Clock()

bulletList = []

wall_list = []

debris = []

def death_function(ship):
    ship.velocity = (0, 0)
    global death_timer
    death_timer = DEATH_TIME
    r = 10
    dspeed = 10
    dtimer = 30
    angles = 360/r
    for i in range(0, r):
        dlocation = ship.location
        dvelocity = (math.sin(math.radians(angles*i))*dspeed, math.cos(math.radians(angles*i))*dspeed)
        debris.append((dlocation, dvelocity, dtimer))

for i in range(0, 100):
    x = random.randint(player_ship.location[0], 3200)
    y = random.randint(player_ship.location[1], 1800)
    w = random.randint(100, 200)
    h = random.randint(100, 200)
    wall_list.append(pygame.Rect(x, y, w, h))
    
wall_list.append(pygame.Rect(0, 0, map_dimensions[0], 25))
wall_list.append(pygame.Rect(0, 0, 25, map_dimensions[1]))
wall_list.append(pygame.Rect(0, map_dimensions[1]-25, map_dimensions[0], 25))
wall_list.append(pygame.Rect(map_dimensions[0]-25, 0, 25, map_dimensions[1]))

# pygame.draw.polygon(display, RED, [(x-dimx, y+dimy), (x+dimx, y+dimy), (x, y-dimy)], 1)
# pygame.display.update()
while True:
    clock.tick(60)
    x, y = player_ship.location
    velx, vely = player_ship.velocity
    dimx, dimy = player_ship.bounds
    display.fill(WHITE)
    moved = False
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
    sinD = math.sin(math.radians(player_ship.direction))
    cosD = math.cos(math.radians(player_ship.direction))
    keys = pygame.key.get_pressed()
    if keys[K_w] or keys[K_UP]:
        player_ship.move()
        moved = True
    if keys[K_a] or keys[K_LEFT]:
        player_ship.turn_left()
    if keys[K_d] or keys[K_RIGHT]:
        player_ship.turn_right()
    if keys[K_SPACE] and player_ship.delay<=0:
        bullet = (x + dimy*sinD, y-dimy*cosD, player_ship.direction, BULLET_DURATION)
        bulletList.append(bullet)
        player_ship.delay = SHOOT_DELAY
        velocity = (velx - SPEED*sinD, vely + SPEED*cosD)
        velx, vely = velocity
        mag = math.sqrt(velx*velx + vely*vely)
        if mag>VELOCITY_CAP:
            velocity = (velx/mag*VELOCITY_CAP, vely/mag*VELOCITY_CAP)
    
    player_ship.update()
    
    for n in wall_list:
        if player_ship.rect.colliderect(n) and death_timer<=0:
            death_function(player_ship)
    
    Display.set_camera_loc(camera, (x, y))
    Display.bound_camera(camera, map_dimensions)
        
    if death_timer<=0:
        Display.draw_triangle(display, camera, BLACK, player_ship.location, player_ship.bounds, player_ship.direction, 2)
        if moved:
            Display.draw_triangle_offset(display, camera, RED, (player_ship.location[0], player_ship.location[1]+player_ship.bounds[1]*3/2), (player_ship.bounds[0]/2, player_ship.bounds[1]/2), player_ship.direction-180, player_ship.location, 2)
    else:
        death_timer-=1
        if death_timer<=0:
            player_ship.location = (320, 240)
            player_ship.velocity = (0, 0)
        
    i = 0
    while i < len(debris):
        debra = debris[i]
        loc = (debra[0][0] + debra[1][0], debra[0][1] + debra[1][1])
        dur = debra[2] - 1
        debris[i] = (loc, debra[1], dur)
        debra = debris[i]
        Display.draw_circle(display, camera, BLACK, debra[0], (30-debra[2])/4 + 3, 2)
        if debra[2]<=0:
            debris.remove(debris[i])
        else:
            i+=1
    
    i = 0
    while i < len(bulletList):
        
        bx, by, bdir, bdur = bulletList[i]
        bsinD = math.sin(math.radians(bdir))
        bcosD = math.cos(math.radians(bdir))
        bdur = bdur - 1
        bulletList[i] = (bx + BULLET_SPEED*bsinD, by - BULLET_SPEED*bcosD, bdir, bdur)
        bx, by, bdir, bdur = bulletList[i]
        rect = pygame.Rect(bx-BULLET_SIZE, by-BULLET_SIZE, BULLET_SIZE*2, BULLET_SIZE*2)
        for n in wall_list:
            if n.colliderect(rect):
                bulletList[i] = (bx, by, bdir, 0)
        if bulletList[i][3]>0:
            Display.draw_circle(display, camera, BLUE, (bx, by), BULLET_SIZE)
        if bdur <= 0:
            bulletList.remove(bulletList[i])
        else:
            i = i+1
    for n in wall_list:
        Display.draw_rect(display, camera, GREEN, n, 2)
    
    pygame.display.update()
