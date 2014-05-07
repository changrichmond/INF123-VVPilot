'''
Created on Apr 29, 2014

@author: john
'''

from Events import Broadcaster

DEATH_TIME = 120

class Logic:
    def __init__(self):
        #event system
        self.onShipDeath = Broadcaster()
        self.onBulletDeath = Broadcaster()
        self.onShipUpdate = Broadcaster()
        self.onBulletUpdate = Broadcaster()
        self.onLogicUpdate = Broadcaster()
        
        #required data
        self.bullet_list = []
        self.wall_list = []
        self.ship_list = []
        
    def doLogic(self):
        for ship in self.ship_list:
            ship.update()
            self.onShipUpdate.fire(ship)
    
        for ship in self.ship_list:
            for n in self.wall_list:
                if ship.rect.colliderect(n) and not ship.isDead():
                    ship.kill(DEATH_TIME)
                    self.onShipDeath.fire(ship)
            for n in self.bullet_list:
                if ship.rect.colliderect(n) and not ship.isDead() and ship is not n.ship:
                    ship.kill(DEATH_TIME)
                    self.onShipDeath.fire(ship)
                    n.duration = 0
    
    
        i = 0
        while i < len(self.bullet_list):
        
            bullet = self.bullet_list[i]
            bullet.update()
            self.onBulletUpdate.fire(bullet)
            for n in self.wall_list:
                if n.colliderect(bullet.rect):
                    bullet.duration = 0
                    self.onBulletDeath.fire(bullet, n)
            if bullet.duration>0:
                i = i+1
            else:
                self.bullet_list.remove(self.bullet_list[i])
        self.onLogicUpdate.fire(self)
        for ship in self.ship_list:
            ship.moved = False
