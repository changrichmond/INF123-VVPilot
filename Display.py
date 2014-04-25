'''
Created on Apr 17, 2014

@author: john
'''

import pygame, math

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
    