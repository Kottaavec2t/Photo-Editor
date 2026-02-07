import customtkinter as ctk
from controllers import EventBus

class BasePanel(ctk.CTkFrame):
    '''
    Base class for panels.

    :param event_bus: The global event_bus to communicate with others scripts.
    :type event_bus: EventBus
    '''
    def __init__(self, master, event_bus: EventBus) -> None:
        super().__init__(master)
        self._event_bus = event_bus
