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

SPEED = 0.075
BULLET_SPEED = 10
BULLET_DURATION = 60
BULLET_SIZE = 5
ANGULAR_VELOCITY = 4
VELOCITY_CAP = 5
SHOOT_DELAY = 10
map_dimensions = (3200, 1800)
camera_bounds = (854, 480)

camera = {'location':(320, 240), 'bounds':camera_bounds}

display = pygame.display.set_mode(camera_bounds)

player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY)
DEATH_TIME = 120
death_timer = 0
death_projectile_count = 10
death_projectile_timer = 30
death_projectile_speed = 5
bullet_debris_timer = 7
bullet_debris_scatter = 90
min_bullet_debris = 2
max_bullet_debris = 5

clock = pygame.time.Clock()

bulletList = []

wall_list = []

debris = []

def calculate_normal(rect, point1, vector):
    #lets solve this using the parametric equation
    point2 = (point1[0] + vector[0], point1[1] + vector[1])
    print 'starting normal calculations'
    print point1
    print point2
    h, k = point1
    p, q = point2
    x1 = p - h
    y1 = q - k
    normal = (1, 0)
    t = 9999999.9999 #a really large number
    if x1 != 0:
        t_temp = math.fabs((rect.right - h)/x1)
        t = t_temp
        print t_temp
        t_temp = math.fabs((rect.left - h)/x1)
        print t_temp
        if t_temp < t:
            t = t_temp
            normal = (-1, 0)
    if y1 != 0:
        t_temp = math.fabs((rect.bottom - k)/y1)
        print t_temp
        if t_temp>=0 and t_temp < t:
            t = t_temp
            normal = (0, 1)
        t_temp = math.fabs((rect.top - k)/y1)
        print t_temp
        if t_temp>=0 and t_temp < t:
            t = t_temp
            normal = (0, -1)
    print normal
    print 'ending normal calculations'
    return normal

def death_function(ship):
    ship.velocity = (0, 0)
    ship.direction = 0
    global death_timer
    death_timer = DEATH_TIME
    angles = 360/death_projectile_count
    for i in range(0, death_projectile_count):
        dlocation = ship.location
        dvelocity = (math.sin(math.radians(angles*i))*death_projectile_speed, math.cos(math.radians(angles*i))*death_projectile_speed)
        scale_factor = 0.25
        scale_base = 3
        thickness = 2
        debris.append((dlocation, dvelocity, death_projectile_timer, scale_factor, scale_base, thickness, death_projectile_timer, BLACK))
        
def bullet_death(bullet, bullet_rect, obstacle_rect, b_vec):
    rand_value = random.randint(min_bullet_debris, max_bullet_debris)
    bd_speed = BULLET_SPEED/2.0
    base_direction = bullet[2]
    base_vel = (math.sin(math.radians(base_direction)), -math.cos(math.radians(base_direction)))
    walln = calculate_normal(obstacle_rect, bullet_rect.center, b_vec)
    wall_dir = math.degrees(math.atan2(walln[1], walln[0])) + 90
    dot = walln[0]*base_vel[0] + walln[1]*base_vel[1]
    reflection = (base_vel[0] - 2 * walln[0]*dot, base_vel[1] - 2*walln[1]*dot)
    ref_dir = math.degrees(math.atan2(reflection[1], reflection[0])) + 90
    for i in range(0, rand_value):
        b_scatter = random.randint(0, bullet_debris_scatter)
        b_speed = random.random()*bd_speed
        direction = ref_dir + b_scatter - bullet_debris_scatter/2
        if(direction > wall_dir + 90):
            direction = wall_dir + 90
        if(direction < wall_dir - 90):
            direction = wall_dir - 90
        dvel = (math.sin(math.radians(direction))*b_speed, -math.cos(math.radians(direction))*b_speed)
        debris.append(((bullet[0], bullet[1]), dvel, bullet_debris_timer, 0, BULLET_SIZE/2, 0,bullet_debris_timer, BLUE))
        

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
    if death_timer<=0:
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
        debris[i] = (loc, debra[1], dur, debra[3], debra[4], debra[5], debra[6], debra[7])
        debra = debris[i]
        Display.draw_circle(display, camera, debra[7], debra[0], int((debra[6]-debra[2])*debra[3]) + debra[4], debra[5])
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
        bspeed = (BULLET_SPEED*bsinD, -BULLET_SPEED*bcosD)
        bulletList[i] = (bx + bspeed[0], by + bspeed[1], bdir, bdur)
        bx, by, bdir, bdur = bulletList[i]
        rect = pygame.Rect(bx-BULLET_SIZE, by-BULLET_SIZE, BULLET_SIZE*2, BULLET_SIZE*2)
        for n in wall_list:
            if n.colliderect(rect):
                bulletList[i] = (bx - bspeed[0], by - bspeed[1], bdir, 0)
                bullet_death(bulletList[i], rect, n, bspeed)
                bx, by, bdir, bdur = bulletList[i]
                rect = pygame.Rect(bx-BULLET_SIZE, by-BULLET_SIZE, BULLET_SIZE*2, BULLET_SIZE*2)
                clip_rect = rect.clip(n)
                if clip_rect.w < clip_rect.h:
                    bx = bx - clip_rect.w
                else:
                    by = by - clip_rect.h
                bx, by, bdir, bdur = bulletList[i]
        if bulletList[i][3]>0:
            Display.draw_circle(display, camera, BLUE, (bx, by), BULLET_SIZE)
        if bdur <= 0:
            bulletList.remove(bulletList[i])
        else:
            i = i+1
    for n in wall_list:
        Display.draw_rect(display, camera, GREEN, n, 2)
    
    pygame.display.update()
