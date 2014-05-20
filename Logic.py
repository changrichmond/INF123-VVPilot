'''
Created on Apr 29, 2014

@author: john
'''

from Events import Broadcaster
from Scoreboard import scoreboard
import Utility

DEATH_TIME = 120

class Logic:
    def __init__(self):
        #event system
        self.onShipDeath = Broadcaster()
        self.onShipKill = Broadcaster()
        self.onBulletDeath = Broadcaster()
        self.onShipUpdate = Broadcaster()
        self.onBulletUpdate = Broadcaster()
        self.onLogicUpdate = Broadcaster()
        
        #required data
        self.bullet_list = []
        self.wall_list = []
        self.ship_list = []
        
        #scoreboard
        self.scoreboard = scoreboard()
        self.onShipDeath+=self.scoreboard.on_ship_death
        self.onShipKill+=self.scoreboard.on_ship_kill
        
    def add_ship(self, ship):
        self.ship_list.append(ship)
        self.scoreboard.add_player(ship)
        
    def calculate_reflection(self, rect, location, velocity):
        normal = Utility.calculate_normal(rect, location, velocity)
        velo = (-1*velocity[0], -1*velocity[1])
        dot_prod = velo[0]*normal[0] + velo[1]*normal[1]
        rvelo = (2*dot_prod*normal[0] - velo[0], 2*dot_prod*normal[1] - velo[1])
        print 'velo'
        print velocity
        print 'relfection velo'
        print rvelo
        return rvelo
        
    def doLogic(self):
        for ship in self.ship_list:
            ship.update()
            self.onShipUpdate.fire(ship)
            
        for i in range(len(self.ship_list)):
            ship1 = self.ship_list[i]
            if not ship1.isDead():
                for j in range(i+1, len(self.ship_list)):
                    ship2 = self.ship_list[j]
                    if not ship2.isDead():
                        if not ship1.shield_obj and not ship2.shield_obj:
                            if ship1.rect.colliderect(ship2.rect):
                                ship1.kill(DEATH_TIME)
                                self.onShipDeath.fire(ship1)
                                ship2.kill(DEATH_TIME)
                                self.onShipDeath.fire(ship2)
                        elif not ship1.shield_obj and ship2.shield_obj:
                            if ship1.rect.colliderect(ship2.shield_obj):
                                ship1.kill(DEATH_TIME)
                                self.onShipDeath.fire(ship1)
                                self.onShipKill.fire(ship1, ship2)
                        elif ship1.shield_obj and not ship2.shield_obj:
                            if ship1.shield_obj.colliderect(ship2.rect):
                                ship2.kill(DEATH_TIME)
                                self.onShipDeath.fire(ship2)
                                self.onShipKill.fire(ship2, ship1)
                        elif ship1.shield_obj and ship2.shield_obj:
                            if ship1.shield_obj.colliderect(ship2.shield_obj):
                                ship1.velocity = self.calculate_reflection(ship2.shield_obj, ship1.location, ship1.velocity)
                                ship2.velocity = self.calculate_reflection(ship1.shield_obj, ship2.location, ship2.velocity)
    
        for ship in self.ship_list:
            if ship.shield_obj:
                for n in self.wall_list:
                    if ship.shield_obj.colliderect(n) and not ship.isDead():
                        velo = self.calculate_reflection(n, ship.location, ship.velocity)
                        ship.velocity = velo
                        overlap = ship.shield_obj.clip(n)
                        if overlap.w < overlap.h:
                            if ship.location[0] > overlap.centerx:
                                ship.location = (ship.location[0] + overlap.w + velo[0], ship.location[1] + velo[1])
                            else:
                                ship.location = (ship.location[0] - overlap.w + velo[0], ship.location[1] + velo[1])
                        else:
                            if ship.location[1] > overlap.centery:
                                ship.location = (ship.location[0] + velo[0], ship.location[1] + overlap.h + velo[1])
                            else:
                                ship.location = (ship.location[0] + velo[0], ship.location[1] - overlap.h + velo[1])
                for n in self.bullet_list:
                    if ship.shield_obj.colliderect(n) and not ship.isDead() and ship is not n.ship:
                        n.duration = 0
            else:
                for n in self.wall_list:
                    if ship.rect.colliderect(n) and not ship.isDead():
                        ship.kill(DEATH_TIME)
                        self.onShipDeath.fire(ship)
                for n in self.bullet_list:
                    if ship.rect.colliderect(n) and not ship.isDead() and ship is not n.ship:
                        ship.kill(DEATH_TIME)
                        self.onShipDeath.fire(ship)
                        self.onShipKill.fire(ship, n.ship)
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
            ship.shield_obj = None
