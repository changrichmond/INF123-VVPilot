'''
Created on May 20, 2014

@author: john
'''

class GameMode:
    
    def __init__(self, scoreboard):
        self.scoreboard = scoreboard
        
    def take_logic(self, logic):
        pass
    
class Deathmatch(GameMode):
    
    def __init__(self, scoreboard):
        GameMode.__init__(self, scoreboard)
        
    def take_logic(self, logic):
        logic.onShipKill+=self.on_ship_kill
        
    def on_ship_kill(self, death_ship, kill_ship):
        self.scoreboard.increment_score(kill_ship)