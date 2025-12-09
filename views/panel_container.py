import customtkinter as ctk
from models.panel_registry import PanelRegistry

class PanelContainer(ctk.CTkFrame):
    ''' Conteneur pour les panneaux latéraux. '''

    def __init__(self, master, event_bus, settings):
        super().__init__(master)

        self.event_bus = event_bus
        self.settings = settings

        self._setup_ui()
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        ''' Setup event subscriptions. '''
        self.event_bus.subscribe("panel_order_changed", self._on_panel_order_changed)

    def _setup_ui(self):
        ''' Setup the UI components of the panel container. '''
        panels_settings = self.settings.get("panels")
        width = panels_settings.get("width", 300)
        self.configure(width=width)

        for panel_name in panels_settings.get("enabled"):
            PanelRegistry.register_panel(panel_name)
            panel_class = PanelRegistry.get_panel(panel_name)
            if panel_class:
                panel_instance = panel_class(self, self.event_bus)
                panel_instance.pack(fill=ctk.X, padx=5, pady=5)
    
    def _on_panel_order_changed(self, data: dict = None):
        ''' Handle changes in panel order. '''
        pass