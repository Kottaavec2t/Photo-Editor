from typing import Callable

class EventBus:
    '''
    An event bus for managing events and listeners.
    '''
    def __init__(self):
        self._listeners = {}
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        '''
        Subscribe a callback to a specific event type.

        :param event_type: The type of event to subscribe to.
        :type event_type: str
        :param callback: The function to call when the event is published.
        :type callback: Callable
        '''
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
    
    def publish(self, event_type: str, data: dict = None) -> None:
        '''
        Publish an event to all subscribed callbacks.
        
        :param event_type: The type of event to publish.
        :type event_type: str
        :param data: Optional data to pass to the callbacks.
        :type data: dict, optional
        '''
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                print('publishing event:', event_type, 'with data:', data)
                callback(data)