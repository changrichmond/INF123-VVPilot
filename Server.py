from network import *
import pygame, random, Serialize
from Logic import Logic
from Ship import Ship
from ServerSideController import ServerSideController

def respawn_func(ship):
    ship.location = (320, 240)
    ship.rect.center = ship.location
    ship.velocity = (0, 0)
    ship.direction = 0
    
def random_respawn(minLoc, maxLoc):
    def respawn(ship):
        ship.location = (random.randint(minLoc[0], maxLoc[0]), random.randint(minLoc[1], maxLoc[1]))
        ship.rect.center = ship.location
        ship.velocity = (0, 0)
        ship.direction = 0
    return respawn

min_respawn = (320, 240)
max_respawn = (3000, 1600)

TICKS = 60
    
SPEED = 0.075
BULLET_SPEED = 10
BULLET_DURATION = 60
BULLET_SIZE = 5
ANGULAR_VELOCITY = 4
VELOCITY_CAP = 5
SHOOT_DELAY = 10
SHIELD_SIZE = 20

map_dimensions = (3200, 1800)

num_walls = 20

handlers = []

logic = Logic()

class EventLog:
    def __init__(self):
        self.bullet_deaths = []
        self.ship_deaths = []
        self.bullet_timeouts = []
        self.wall_reflects = []
        self.ship_reflects = []
        
    def ship_log(self, ship):
        self.ship_deaths.append((ship, logic.current_tick))
        
    def bullet_log(self, bullet, wall):
        self.bullet_deaths.append((bullet,wall, logic.current_tick))
    
    def bullet_timeout(self, bullet):
        self.bullet_timeouts.append((bullet, logic.current_tick))
        
    def wall_reflect_log(self, ship, wall):
        self.wall_reflects.append((ship, wall, logic.current_tick))
    
    def ship_reflect_log(self, ship1, ship2):
        self.ship_reflects.append((ship1, ship2, logic.current_tick))

event_log = EventLog()
logic.onShipDeath+=event_log.ship_log
logic.onBulletDeath+=event_log.bullet_log
logic.onBulletTimeout+=event_log.bullet_timeout
logic.onShipReflectShip+=event_log.ship_reflect_log
logic.onShipReflectWall+=event_log.wall_reflect_log

class MyHandler(Handler):
    
    def on_open(self):
        # Grouped together to handle multiple players (new connection)
        player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY, random_respawn(min_respawn, max_respawn))
        logic.ship_list.append(player_ship)
        self.controller = ServerSideController(player_ship, logic, BULLET_SIZE, BULLET_SPEED, BULLET_DURATION, SHOOT_DELAY, SHIELD_SIZE)
        logic.onLogicUpdate+=self.controller.update
        self.do_send({'start': { 'walls': [Serialize.serializeRect(wall) for wall in logic.wall_list],
                                'ticks': TICKS, 
                                'speed' : SPEED,
                                'bspeed' : BULLET_SPEED,
                                'maxvelo' : VELOCITY_CAP,
                                'angular' : ANGULAR_VELOCITY,
                                'current' : logic.current_tick,
                                'id' : player_ship.id}})
        #logic.onLogicUpdate+=self.onLogicUpdate
        handlers.append(self)
     
#     def onLogicUpdate(self, logic):
#         pass
# #         msg = {'update':
# #                {'ships': [Serialize.serializeShip(ship) for ship in logic.ship_list], 
# #                 'bullets': [Serialize.serializeBullet(bullet) for bullet in logic.bullet_list], 
# #                 'location': self.controller.player_ship.location,
# #                  'ship_deaths': [Serialize.serializeShip(ship) for ship in event_log.ship_deaths], 
# #                  'bullet_deaths': [(Serialize.serializeBullet(bullet[0]), Serialize.serializeRect(bullet[1])) for bullet in event_log.bullet_deaths ]} }
# #         self.do_send(msg)
              
    def on_close(self):
        logic.ship_list.remove(self.controller.player_ship)
     
    def on_msg(self, msg):
        if 'control' in msg:
            if msg['control'] == 'move_on':
                self.controller.isMoving = True
                self.controller.player_ship.moved = True
            elif msg['control'] == 'left_on':
                self.controller.isLefting = True
            elif msg['control'] == 'right_on':
                self.controller.isRighting = True
            elif msg['control'] == 'shoot_on':
                self.controller.isShooting = True
            elif msg['control'] == 'shield_on':
                self.controller.isShielding = True
            elif msg['control'] == 'move_off':
                self.controller.isMoving = False
                self.controller.player_ship.moved = False
            elif msg['control'] == 'left_off':
                self.controller.isLefting = False
            elif msg['control'] == 'right_off':
                self.controller.isRighting = False
            elif msg['control'] == 'shoot_off':
                self.controller.isShooting = False
            elif msg['control'] == 'shield_off':
                self.controller.isShielding = False
                self.controller.player_ship.shield_obj = None
#         if 'control' in msg:
#             if msg['control'] == 'move':
#                 self.controller.move_ship()
#             elif msg['control'] == 'left':
#                 self.controller.turn_left()
#             elif msg['control'] == 'right':
#                 self.controller.turn_right()
#             elif msg['control'] == 'shoot':
#                 self.controller.shoot()
#             elif msg['control'] == 'shield_on':
#                 self.controller.shield_on()

def poll_events():
    event_list = []
    for h in handlers:
        event_list.extend(h.controller.log)
        h.controller.log = []
    ship_output = {}
    bullet_output = {}
    for e in event_list:
        if e[0] == 'ship':
            if not ship_output.has_key('normal'):
                ship_output['normal'] = []
            ship_output['normal'].append((Serialize.serializeShip(e[1]), e[2], e[3], e[4], e[5]))
        elif e[0] == 'bullet':
            if not bullet_output.has_key('normal'):
                bullet_output['normal'] = []
            bullet_output['normal'].append((Serialize.serializeBullet(e[1]), e[2]))
            
    for e in event_log.ship_deaths:
        if not ship_output.has_key('death'):
            ship_output['death'] = []
        ship_output['death'].append((Serialize.serializeShip(e[0]), e[1], False, False, False))
    event_log.ship_deaths = []
    
    for e in event_log.ship_reflects:
        if not ship_output.has_key('reflect'):
            ship_output['reflect'] = []
        ship_output['reflect'].append((Serialize.serializeShip(e[0]), e[2]))
        ship_output['reflect'].append((Serialize.serializeShip(e[1]), e[2]))
    event_log.ship_reflects = []
        
    for e in event_log.wall_reflects:
        if not ship_output.has_key('reflect'):
            ship_output['reflect'] = []
        ship_output['reflect'].append((Serialize.serializeShip(e[0]), e[2]))
    event_log.wall_reflects = []
        
    for e in event_log.bullet_deaths:
        if not bullet_output.has_key('death'):
            bullet_output['death'] = []
        bullet_output['death'].append((Serialize.serializeBullet(e[0]), Serialize.serializeRect(e[1]), e[2]))
    event_log.bullet_deaths = []
    
    for e in event_log.bullet_timeouts:
        if not bullet_output.has_key('timeout'):
            bullet_output['timeout'] = []
        bullet_output['timeout'].append((Serialize.serializeBullet(e[0]), e[1]))
    event_log.bullet_timeouts = []
        
    full_output = {}
    if len(ship_output)>0:
        full_output['ship'] = ship_output
    if len(bullet_output)>0:
        full_output['bullet'] = bullet_output
    if len(full_output)>0:
        msg = { 'update' : full_output }
        for h in handlers:
            h.do_send(msg)
    
            
    
        

for i in range(0, num_walls):
    x = random.randint(400, 3200)
    y = random.randint(400, 1800)
    w = random.randint(100, 200)
    h = random.randint(100, 200)
    logic.wall_list.append(pygame.Rect(x, y, w, h))
    
logic.wall_list.append(pygame.Rect(0, 0, map_dimensions[0], 25))
logic.wall_list.append(pygame.Rect(0, 0, 25, map_dimensions[1]))
logic.wall_list.append(pygame.Rect(0, map_dimensions[1]-25, map_dimensions[0], 25))
logic.wall_list.append(pygame.Rect(map_dimensions[0]-25, 0, 25, map_dimensions[1]))

port = 8888
server = Listener(port, MyHandler)
clock = pygame.time.Clock()
while 1:
    clock.tick(TICKS)
    logic.doLogic()
    poll_events()
#     event_log.bullet_deaths = []
#     event_log.ship_deaths = []
    poll(timeout=0.0125) # in seconds