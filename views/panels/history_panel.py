import customtkinter as ctk
from views.panels import BasePanel
from controllers import EventBus

class HistoryPanel(BasePanel):
    '''
    Panel for viewing photo edit history.

    :param event_bus: The global event_bus to communicate with others scripts.
    :type event_bus: EventBus
    '''
    def __init__(self, master, event_bus: EventBus) -> None:
        super().__init__(master, event_bus)
        self._event_bus = event_bus
        self._setup_ui()
