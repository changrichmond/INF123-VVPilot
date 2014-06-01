'''
Created on Apr 30, 2014

@author: john
'''

import pygame, Serialize, time, math
from pygame.locals import *
from network import *

from View import View

from Events import Broadcaster

class ClientEventSystem():
    def __init__(self):
        self.onShipDeath = Broadcaster()
        self.onBulletDeath = Broadcaster()
    
class ClientController():
    def __init__(self, handler):
        self.handler = handler
    def move_ship(self):
        self.handler.do_send({'control':'move_on'})
    
    def turn_left(self):
        self.handler.do_send({'control':'left_on'})
    
    def turn_right(self):
        self.handler.do_send({'control':'right_on'})
    
    def shoot(self):
        self.handler.do_send({'control':'shoot_on'})
        
    def shield(self):
        self.handler.do_send({'control':'shield_on'})
    
    def stop_move_ship(self):
        self.handler.do_send({'control':'move_off'})
        
    def stop_turn_left(self):
        self.handler.do_send({'control':'left_off'})
    
    def stop_turn_right(self):
        self.handler.do_send({'control':'right_off'})
    
    def stop_shoot(self):
        self.handler.do_send({'control':'shoot_off'})
        
    def stop_shield(self):
        self.handler.do_send({'control':'shield_off'})
        
running = 1

TICKS = 60

SERVER_TICKS = TICKS
    
SPEED = 0
BULLET_SPEED = 0
ANGULAR_VELOCITY = 0
VELOCITY_CAP = 0

server_current = 0

def interpolate_ship(ship, delta, flags):
    for n in range(delta):
        if flags[1]:
            ship.direction -= ANGULAR_VELOCITY
        if flags[2]:
            ship.direction += ANGULAR_VELOCITY
        ship.location = (ship.location[0] + ship.velocity[0]*delta, ship.location[1] + ship.velocity[1]*delta)
        if flags[0]:
            sinD = math.sin(math.radians(ship.direction))
            cosD = math.cos(math.radians(ship.direction))
            ship.velocity = (ship.velocity[0] + SPEED*sinD, ship.velocity[1] - SPEED*cosD)
            mag = math.sqrt(math.pow(ship.velocity[0], 2) + math.pow(ship.velocity[1], 2))
            if mag>VELOCITY_CAP:
                ship.velocity = (ship.velocity[0]/mag*VELOCITY_CAP, ship.velocity[1]/mag*VELOCITY_CAP)
        if ship.shield_obj:
            ship.shield_obj.center = ship.location

def interpolate_bullet(bullet, delta):
    for n in range(delta):
        bullet.update()
#     ship.direction += ANGULAR_VELOCITY*delta
#     velocity = ship.velocity
#     if isMoving:
#         ship.move_from_force(SPEED*delta)
#     
#     ship.location = (ship.location[0] + ship.velocity[0]*delta, ship.location[1] + ship.velocity[1]*delta)
    

ship_dict = {}
flags_dict = {}
bullet_dict = {}

class Client(Handler):
    def __init__(self, host, port, view, client_controller):
        Handler.__init__(self, host, port)
        self.view = view
        self.controller = client_controller
        self.ship_id = 0
    
    def on_close(self):
        global running
        running = 0
    
    def on_msg(self, msg):
        if 'start' in msg:
            global SERVER_TICKS, SPEED, BULLET_SPEED, VELOCITY_CAP, ANGULAR_VELOCITY
            SERVER_TICKS = msg['start']['ticks']
            SPEED = msg['start']['speed']
            BULLET_SPEED = msg['start']['bspeed']
            VELOCITY_CAP = msg['start']['maxvelo']
            ANGULAR_VELOCITY = msg['start']['angular']
            server_current = msg['start']['current']
            self.ship_id = msg['start']['id']
            for wall in msg['start']['walls']:
                self.view.wall_list.append(Serialize.deserializeRect(wall))
            
        elif 'update' in msg:
            msginput = msg['update']
            if 'ship' in msginput:
                if 'normal' in msginput['ship']:
                    for n in msginput['ship']['normal']:
                        ship = Serialize.deserializeShip(n[0])
                        isMoving = n[2]
                        isLefting = n[3]
                        isRighting = n[4]
                        if ship.id in ship_dict:
                            found_ship = ship_dict[ship.id]
                            found_ship.__dict__ = ship.__dict__.copy()
                        else:
                            ship_dict[ship.id] = ship
                            self.view.ship_list.append(ship)
                            
                        flags_dict[ship.id] = (isMoving, isLefting, isRighting)
                if 'death' in msginput['ship']:
                    for n in msginput['ship']['death']:
                        ship = Serialize.deserializeShip(n[0])
                        isMoving = n[2]
                        isLefting = n[3]
                        isRighting = n[4]
                        if ship.id in ship_dict:
                            found_ship = ship_dict[ship.id]
                            found_ship.__dict__ = ship.__dict__.copy()
                        else:
                            ship_dict[ship.id] = ship
                            self.view.ship_list.append(ship)
                        flags_dict[ship.id] = (isMoving, isLefting, isRighting)
                        self.controller.onShipDeath.fire(ship)
            if 'bullet' in msginput:
                if 'normal' in msginput['bullet']:
                    for n in msginput['bullet']['normal']:
                        bullet = Serialize.deserializeBullet(n[0])
                        if bullet.id in bullet_dict:
                            found_bullet = bullet_dict[bullet.id]
                            found_bullet.__dict__ = bullet.__dict__.copy()
                        else:
                            bullet_dict[bullet.id] = bullet
                            self.view.bullet_list.append(bullet)
                if 'death' in msginput['bullet']:
                    for n in msginput['bullet']['death']:
                        bullet = Serialize.deserializeBullet(n[0])
                        wall = Serialize.deserializeRect(n[1])
                        self.controller.onBulletDeath.fire(bullet, wall)  
                if 'timeout' in msginput['bullet']:
                    for n in msginput['bullet']['timeout']:
                        bullet = Serialize.deserializeBullet(n[0])
                        if bullet.id in bullet_dict:
                            self.view.bullet_list.remove(bullet_dict[bullet.id])
                            del bullet_dict[bullet.id]
#             self.view.ship_list = [Serialize.deserializeShip(ship) for ship in msg['update']['ships']]
#             self.view.bullet_list = [Serialize.deserializeBullet(bullet) for bullet in msg['update']['bullets']]
#             self.view.set_camera_loc(msg['update']['location'])
#             for ship_ID in msg['update']['ship_deaths']:
#                 self.controller.onShipDeath.fire(Serialize.deserializeShip(ship_ID))
#             for bullet_ID in msg['update']['bullet_deaths']:
#                 self.controller.onBulletDeath.fire(Serialize.deserializeBullet(bullet_ID[0]), Serialize.deserializeRect(bullet_ID[1]))                                                                           

map_dimensions = (3200, 1800)

camera_bounds = (854, 480)

frame_rate = 60.0
frame_duration = 1.0/frame_rate

cevent = ClientEventSystem()
view = View(camera_bounds, cevent, map_dimensions)
host, port = 'localhost', 8888
client = Client(host, port, view, cevent)

controller = ClientController(client)

def read_inputs(onMove, onTurnLeft, onTurnRight, onShoot, onShield, offMove, offTurnLeft, offTurnRight, offShoot, offShield):
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:
                onMove()
            elif event.key == K_a or event.key == K_LEFT:
                onTurnLeft()
            elif event.key == K_d or event.key == K_RIGHT:
                onTurnRight()
            elif event.key == K_SPACE:
                onShoot()
            elif event.key == K_s or event.key == K_DOWN:
                onShield()
        elif event.type == KEYUP:
            if event.key == K_w or event.key == K_UP:
                offMove()
            elif event.key == K_a or event.key == K_LEFT:
                offTurnLeft()
            elif event.key == K_d or event.key == K_RIGHT:
                offTurnRight()
            elif event.key == K_SPACE:
                offShoot()
            elif event.key == K_s or event.key == K_DOWN:
                offShield()


def read_input(onMove, onTurnLeft, onTurnRight, onShoot, onShield):
    keys = pygame.key.get_pressed()
    if keys[K_w] or keys[K_UP]:
        onMove()
    if keys[K_a] or keys[K_LEFT]:
        onTurnLeft()
    if keys[K_d] or keys[K_RIGHT]:
        onTurnRight()
    if keys[K_SPACE]:
        onShoot()
    if keys[K_s]:
        onShield()

# view.wall_list = logic.wall_list
# view.bullet_list = logic.bullet_list
# view.ship_list = logic.ship_list

# def periodic_poll():
#     while 1:
#         poll(timeout=0.0125)
# 
# clock = pygame.time.Clock()
# thread = Thread(target=periodic_poll)
# thread.daemon = True  # die when the main thread dies 
# thread.start()
while running:
    start_time = time.time()
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#     player_ship.moved = False
    read_inputs(controller.move_ship, controller.turn_left, controller.turn_right, controller.shoot, controller.shield, 
                controller.stop_move_ship, controller.stop_turn_left, controller.stop_turn_right, controller.stop_shoot, controller.stop_shield)
    
    for n in view.ship_list:
        interpolate_ship(n, 1, flags_dict[n.id])
    for n in view.bullet_list:
        interpolate_bullet(n, 1)
    if client.ship_id in ship_dict:
        view.set_camera_loc(ship_dict[client.ship_id].location)
    view.draw_everything()
    while time.time() - start_time < frame_duration:
        poll(frame_duration - (time.time() - start_time))