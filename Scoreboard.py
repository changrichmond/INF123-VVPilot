'''
Created on May 19, 2014

@author: john
'''

class scoreboard:
    
    def __init__(self):
        self.score_map = {}
        
    def add_player(self, ship):
        # tuple is (kills, deaths, score)
        self.score_map[ship] = (0, 0, 0)
        
    def on_ship_death(self, ship):
        if ship in self.score_map:
            tup = self.score_map[ship]
            self.score_map[ship] = (tup[0], tup[1]+1, tup[2])
        
    def on_ship_kill(self, dead_ship, kill_ship):
        if kill_ship in self.score_map:
            tup = self.score_map[kill_ship]
            self.score_map[kill_ship] = (tup[0]+1, tup[1], tup[2])
