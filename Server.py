from network import *
import pygame, random
from Logic import Logic
from Ship import Ship
from ServerSideController import ServerSideController

def respawn_func(ship):
    ship.location = (320, 240)
    ship.rect.center = ship.location
    ship.velocity = (0, 0)
    ship.direction = 0
    
SPEED = 0.075
BULLET_SPEED = 10
BULLET_DURATION = 60
BULLET_SIZE = 5
ANGULAR_VELOCITY = 4
VELOCITY_CAP = 5
SHOOT_DELAY = 10

map_dimensions = (3200, 1800)

handlers = []

logic = Logic()

class EventLog:
    def __init__(self):
        self.bullet_deaths = []
        self.ship_deaths = []
        
    def ship_log(self, ship):
        self.ship_deaths.append(ship)
        
    def bullet_log(self, bullet, wall):
        self.bullet_deaths.append((bullet,wall))

event_log = EventLog()
logic.onShipDeath+=event_log.ship_log
logic.onBulletDeath+=event_log.bullet_log

class MyHandler(Handler):
    
    def on_open(self):
        # Grouped together to handle multiple players (new connection)
        player_ship = Ship((320, 240), (15, 15), SHOOT_DELAY, SPEED, VELOCITY_CAP, ANGULAR_VELOCITY, respawn_func)
        logic.ship_list.append(player_ship)
        self.controller = ServerSideController(player_ship, logic, BULLET_SIZE, BULLET_SPEED, BULLET_DURATION, SHOOT_DELAY)
        self.do_send({'start': logic.wall_list})
        logic.onLogicUpdate+=self.onLogicUpdate
     
    def onLogicUpdate(self, logic):
        msg = {'update':
               {'ships': logic.ship_list, 'bullets': logic.bullet_list, 'location': self.controller.player_ship.location,
                 'ship_deaths': event_log.ship_deaths, 'bullet_deaths': event_log.bullet_deaths} }
              
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        pass



for i in range(0, 100):
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
    clock.tick(60)
    logic.doLogic()
    poll(timeout=0.05) # in seconds