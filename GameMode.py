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
        if kill_ship in self.scoreboard.score_map:
            tup = self.scoreboard.score_map[kill_ship]
            self.scoreboard.score_map[kill_ship] = (tup[0], tup[1], tup[2]+1)