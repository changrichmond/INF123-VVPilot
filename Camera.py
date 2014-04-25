'''
Created on Apr 24, 2014

@author: Cory
'''

class Camera:
    
    def __init__(self, location, bounds):
        self.location = location
        self.bounds = bounds
    
    def set_camera_loc(self, location):
        self.location = location
        
    def bound_camera(self, map_bounds):
        camx, camy = self.location
        camw, camh = self.bounds
        
        if camx - camw/2 < 0:
            self.location = (camw/2, camy)
        elif camx + camw/2 > map_bounds[0]:
            self.location = (map_bounds[0] - camw/2, camy)
        if camy - camh/2 < 0:
            self.location = (self.location[0], camh/2)
        elif camy + camh/2 > map_bounds[1]:
            self.location = (self.location[0], map_bounds[1] - camh/2)