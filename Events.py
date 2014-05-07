'''
Created on May 6, 2014

@author: john
'''

class Broadcaster:
    def __init__(self):
        self.handlers = []
        
    def __iadd__(self, handler):
        self.handlers.append(handler)
        return self
    
    def __isub__(self, handler):
        self.handlers.remove(handler)
        return self
    
    def fire(self, *args):
        for n in self.handlers:
            n(*args)

class EventManager:
    
    def __init__(self):
        self.listeners = {}
        
    def subscribe(self, event_type, event_listener):
        if not self.listeners.has_key(event_type):
            self.listeners[event_type] = []
        self.listeners[event_type].append(event_listener)
        
    def unsubscribe(self, event_type, event_listener):
        self.listeners[event_type].pop(self.listeners[event_type].index(event_listener))
        
    def publish(self, event_type, args):
        for n in self.listeners[event_type]:
            n(args)