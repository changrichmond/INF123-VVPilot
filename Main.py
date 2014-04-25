'''
Created on Apr 2, 2014

@author: Cory
'''
import pygame, math, random
import pygame.gfxdraw
from pygame.locals import *
import Display
from Ship import Ship
from Camera import Camera
from Bullet import Bullet

def respawn_func(ship):
    ship.location = (320, 240)
    ship.rect.center = ship.location
    ship.velocity = (0, 0)
    ship.direction = 0

pygame.init()
pygame.key.set_repeat(15,15)

RED = (255,0,0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SPEED = 0.075
BULLET_SPEED = 10
BULLET_DURATION = 60
BULLET_SIZE = 5
ANGULAR_VELOCITY = 4
VELOCITY_CAP = 5
SHOOT_DELAY = 10
map_dimensions = (3200, 1800)
camera_bounds = (854, 480)
camera_start_location = (320, 240)

# camera = {'location':(320, 240), 'bounds':camera_bounds}
camera = Camera(camera_start_location, camera_bounds)

#we legit now son
pygame.display.set_caption("VV Pilot")

icon = pygame.Surface((32, 32))
icon.fill(WHITE)
pygame.gfxdraw.polygon(icon, ((3, 29), (29, 29), (16, 3)), BLACK)
pygame.gfxdraw.polygon(icon, ((4, 28), (28, 28), (16, 3)), BLACK)
pygame.gfxdraw.aapolygon(icon, ((2, 30), (30, 30), (15, 2)), BLACK)
pygame.display.set_icon(icon)

display = pygame.display.set_mode(camera_bounds)

player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY, respawn_func)
DEATH_TIME = 120

clock = pygame.time.Clock()

bulletList = []

wall_list = []

debris = []
        

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
    if not player_ship.isDead():
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
            bullet = Bullet((x + dimy*sinD, y-dimy*cosD), (BULLET_SIZE, BULLET_SIZE), player_ship.direction, (BULLET_SPEED*sinD, -BULLET_SPEED*cosD), BULLET_DURATION)
            #bullet = (x + dimy*sinD, y-dimy*cosD, player_ship.direction, BULLET_DURATION)
            bulletList.append(bullet)
            player_ship.delay = SHOOT_DELAY
            player_ship.move_from_force_in_direction(player_ship.acceleration, player_ship.direction+180)
    
    player_ship.update()
    
    for n in wall_list:
        if player_ship.rect.colliderect(n) and not player_ship.isDead():
            player_ship.kill(DEATH_TIME)
            Display.death_animation(player_ship, debris, BLACK)
    
    camera.set_camera_loc((x, y))
    camera.bound_camera(map_dimensions)
        
    if not player_ship.isDead():
        Display.draw_triangle(display, camera, BLACK, player_ship.location, player_ship.bounds, player_ship.direction, 2)
        if moved:
            Display.draw_triangle_offset(display, camera, RED, (player_ship.location[0], player_ship.location[1]+player_ship.bounds[1]*3/2), (player_ship.bounds[0]/2, player_ship.bounds[1]/2), player_ship.direction-180, player_ship.location, 2)
        
    i = 0
    while i < len(debris):
        debra = debris[i]
        loc = (debra[0][0] + debra[1][0], debra[0][1] + debra[1][1])
        dur = debra[2] - 1
        debris[i] = (loc, debra[1], dur, debra[3], debra[4], debra[5], debra[6], debra[7])
        debra = debris[i]
        Display.draw_circle(display, camera, debra[7], debra[0], int((debra[6]-debra[2])*debra[3]) + debra[4], debra[5])
        if debra[2]<=0:
            debris.remove(debris[i])
        else:
            i+=1
    
    i = 0
    while i < len(bulletList):
        
        bullet = bulletList[i]
        bullet.update()
        for n in wall_list:
            if n.colliderect(bullet.rect):
                bullet.duration = 0
                Display.bullet_death(bulletList[i], bullet.rect, n, bullet.velocity, BULLET_SIZE/2, debris, BLUE)
        if bullet.duration>0:
            Display.draw_circle(display, camera, BLUE, bullet.location, BULLET_SIZE)
            i = i+1
        else:
            bulletList.remove(bulletList[i])
    for n in wall_list:
        Display.draw_rect(display, camera, GREEN, n, 2)
    
    pygame.display.update()
