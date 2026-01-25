'''Module for managing events connections.'''

class EventBus:
    '''A simple event bus for managing events and listeners.'''
    def __init__(self):
        self._listeners = {}
    
    def subscribe(self, event_type: str, callback):
        '''Subscribe a callback to a specific event type.'''
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
    
    def publish(self, event_type: str, data: dict = None):
        '''Publish an event to all subscribed callbacks.'''
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                print('publishing event:', event_type, 'with data:', data)
                callback(data)