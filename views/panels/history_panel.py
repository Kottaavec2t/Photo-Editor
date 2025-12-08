import customtkinter as ctk
from views.panels.base_panel import BasePanel

class HistoryPanel(BasePanel):
    ''' Panel for viewing photo edit history. '''

    def __init__(self, master, event_bus):
        super().__init__(master, event_bus)
        self.event_bus = event_bus
        self._setup_ui()