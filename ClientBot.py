'''
Created on May 27, 2014

@author: john
'''

import random, Serialize, time
# from threading import Thread
from network import *

# from View import View
from Ship import Ship

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

class DumbView:
    def __init__(self):
        self.wall_list = []
        self.bullet_list = []
        self.ship_list = []
        
    def set_camera_loc(self, location):
        pass

class Client(Handler):
    def __init__(self, host, port, view, client_controller):
        Handler.__init__(self, host, port)
        self.view = view
        self.controller = client_controller
    
    def on_close(self):
        global running
        running = 0
    
    def on_msg(self, msg):
        if 'start' in msg:
            for wall in msg['start']:
                self.view.wall_list.append(Serialize.deserializeRect(wall))
        elif 'update' in msg:
            self.view.ship_list = [Serialize.deserializeShip(ship) for ship in msg['update']['ships']]
            self.view.bullet_list = [Serialize.deserializeBullet(bullet) for bullet in msg['update']['bullets']]
            self.view.set_camera_loc(msg['update']['location'])
            for ship_ID in msg['update']['ship_deaths']:
                self.controller.onShipDeath.fire(Serialize.deserializeShip(ship_ID))
            for bullet_ID in msg['update']['bullet_deaths']:
                self.controller.onBulletDeath.fire(Serialize.deserializeBullet(bullet_ID[0]), Serialize.deserializeRect(bullet_ID[1]))                                                                           

map_dimensions = (3200, 1800)

camera_bounds = (854, 480)

frame_rate = 60.0
frame_duration = 1.0/frame_rate

cevent = ClientEventSystem()
# view = View(camera_bounds, cevent, map_dimensions)
host, port = raw_input('input IP address'), 8888
client = Client(host, port, DumbView(), cevent)

controller = ClientController(client)

class client_bot:
    def __init__(self):
        self.isMoving = False
        self.isLefting = False
        self.isRighting = False
        self.isShooting = False
        self.isShielding = False
        
    def read_inputs(self, onMove, onTurnLeft, onTurnRight, onShoot, onShield, offMove, offTurnLeft, offTurnRight, offShoot, offShield):
        value = random.randint(0, 100)
        if value<=20:
            if self.isMoving:
                offMove()
            else:
                onMove()
        elif value<=40:
            if self.isLefting:
                offTurnLeft()
            else:
                onTurnLeft()
        elif value<=60:
            if self.isRighting:
                offTurnRight()
            else:
                onTurnRight()
        elif value<=80:
            if self.isShooting:
                offShoot()
            else:
                onShoot()
        else:
            if self.isShielding:
                offShield()
            else:
                onShield()
            

# def read_inputs(onMove, onTurnLeft, onTurnRight, onShoot, onShield, offMove, offTurnLeft, offTurnRight, offShoot, offShield):
#     
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#         elif event.type == KEYDOWN:
#             if event.key == K_w or event.key == K_UP:
#                 onMove()
#             elif event.key == K_a or event.key == K_LEFT:
#                 onTurnLeft()
#             elif event.key == K_d or event.key == K_RIGHT:
#                 onTurnRight()
#             elif event.key == K_SPACE:
#                 onShoot()
#             elif event.key == K_s or event.key == K_DOWN:
#                 onShield()
#         elif event.type == KEYUP:
#             if event.key == K_w or event.key == K_UP:
#                 offMove()
#             elif event.key == K_a or event.key == K_LEFT:
#                 offTurnLeft()
#             elif event.key == K_d or event.key == K_RIGHT:
#                 offTurnRight()
#             elif event.key == K_SPACE:
#                 offShoot()
#             elif event.key == K_s or event.key == K_DOWN:
#                 offShield()


# def read_input(onMove, onTurnLeft, onTurnRight, onShoot, onShield):
#     keys = pygame.key.get_pressed()
#     if keys[K_w] or keys[K_UP]:
#         onMove()
#     if keys[K_a] or keys[K_LEFT]:
#         onTurnLeft()
#     if keys[K_d] or keys[K_RIGHT]:
#         onTurnRight()
#     if keys[K_SPACE]:
#         onShoot()
#     if keys[K_s]:
#         onShield()

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
bot = client_bot()
while running:
    start_time = time.time()
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#     player_ship.moved = False
    bot.read_inputs(controller.move_ship, controller.turn_left, controller.turn_right, controller.shoot, controller.shield, 
                controller.stop_move_ship, controller.stop_turn_left, controller.stop_turn_right, controller.stop_shoot, controller.stop_shield)
    
#     view.draw_everything()
    while time.time() - start_time < frame_duration:
        poll(frame_duration - (time.time() - start_time))