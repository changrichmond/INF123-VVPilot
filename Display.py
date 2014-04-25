'''
Created on Apr 17, 2014

@author: john
'''

import pygame, math, random
import Utility

death_projectile_count = 10
death_projectile_timer = 30
death_projectile_speed = 10

bullet_debris_timer = 12
bullet_debris_scatter = 180
bullet_debris_speed_min = 1
bullet_debris_speed_max = 3
bullet_debris_speed_range = bullet_debris_speed_max - bullet_debris_speed_min
min_bullet_debris = 2
max_bullet_debris = 5

def draw_rect(display, camera, color, rect, thickness = 0):
    cameraLocation = camera.location
    cameraBounds = camera.bounds
    drawRect = pygame.Rect(rect.x-(cameraLocation[0]-cameraBounds[0]/2), rect.y-(cameraLocation[1]-cameraBounds[1]/2), rect.w, rect.h)
    pygame.draw.rect(display, color, drawRect, thickness)
    
def draw_triangle(display, camera, color, location, dimensions, angle, thickness = 0):
    draw_triangle_offset(display, camera, color, location, dimensions, angle, location, thickness)
    
def draw_triangle_offset(display, camera, color, location, dimensions, angle, rotate_point, thickness = 0):
    cameraLocation = camera.location
    cameraBounds = camera.bounds
    camx = cameraLocation[0] - cameraBounds[0]/2
    camy = cameraLocation[1] - cameraBounds[1]/2
    offsetx = rotate_point[0] - location[0]
    offsety = rotate_point[1] - location[1]
    dimx, dimy = dimensions
    x, y = rotate_point
    point1 = (-dimx + offsetx, dimy + offsety)
    point2 = (dimx + offsetx, dimy + offsety)
    point3 = (offsetx, -dimy + offsety)
    sinD = math.sin(math.radians(angle))
    cosD = math.cos(math.radians(angle))
    x1 = point1[0]*cosD - point1[1]*sinD
    y1 = point1[0]*sinD + point1[1]*cosD
    x2 = point2[0]*cosD - point2[1]*sinD
    y2 = point2[0]*sinD + point2[1]*cosD
    x3 = point3[0]*cosD - point3[1]*sinD
    y3 = point3[0]*sinD + point3[1]*cosD
    pygame.draw.polygon(display, color, [(x-camx+x1, y-camy+y1), (x-camx+x2, y-camy+y2), (x-camx+x3, y-camy+y3)], thickness)
    
def draw_circle(display, camera, color, location, radius, thickness = 0):
    cameraLocation = camera.location
    cameraBounds = camera.bounds
    camx = cameraLocation[0] - cameraBounds[0]/2
    camy = cameraLocation[1] - cameraBounds[1]/2
    pygame.draw.circle(display, color, (int(location[0]-camx), int(location[1]-camy)), radius, thickness)
    
def death_function(ship, debris, color):
    ship.velocity = (0, 0)
    ship.direction = 0
    angles = 360/death_projectile_count
    for i in range(0, death_projectile_count):
        dlocation = ship.location
        dvelocity = (math.sin(math.radians(angles*i))*death_projectile_speed, math.cos(math.radians(angles*i))*death_projectile_speed)
        scale_factor = 0.25
        scale_base = 3
        thickness = 2
        debris.append((dlocation, dvelocity, death_projectile_timer, scale_factor, scale_base, thickness, death_projectile_timer, color))
        
def bullet_death(bullet, bullet_rect, obstacle_rect, b_vec, bullet_size, debris, color):
    rand_value = random.randint(min_bullet_debris, max_bullet_debris)
    base_direction = bullet.direction
    base_vel = (math.sin(math.radians(base_direction)), -math.cos(math.radians(base_direction)))
    walln = Utility.calculate_normal(obstacle_rect, bullet_rect.center, b_vec)
    wall_dir = math.degrees(math.atan2(walln[1], walln[0])) + 90
    dot = walln[0]*base_vel[0] + walln[1]*base_vel[1]
    reflection = (base_vel[0] - 2 * walln[0]*dot, base_vel[1] - 2*walln[1]*dot)
    ref_dir = math.degrees(math.atan2(reflection[1], reflection[0])) + 90
    for i in range(0, rand_value):
        b_scatter = random.randint(0, bullet_debris_scatter)
        b_speed = random.random()*bullet_debris_speed_range + bullet_debris_speed_min
        direction = ref_dir + b_scatter - bullet_debris_scatter/2
        if(direction > wall_dir + 90):
            direction = wall_dir + 90
        if(direction < wall_dir - 90):
            direction = wall_dir - 90
        dvel = (math.sin(math.radians(direction))*b_speed, -math.cos(math.radians(direction))*b_speed)
        debris.append((bullet.location, dvel, bullet_debris_timer, 0, bullet_size, 0, bullet_debris_timer, color))
    