import customtkinter as ctk
from controllers import EventBus
from models import (
    PanelRegistry,
    SettingsManager,
)

class PanelContainer(ctk.CTkFrame):
    '''
    Lateral Panel container.

    :param event_bus: The global event_bus to communicate with others scripts.
    :type event_bus: EventBus
    :param settings: The global settings manager to access settings from nowhere.
    :type settings: SettingsManager
    '''
    def __init__(self, master, event_bus: EventBus, settings: SettingsManager) -> None:
        super().__init__(master)

        self._event_bus = event_bus
        self._settings = settings

        self._setup_ui()
        self._setup_subscriptions()

    def _setup_subscriptions(self) -> None:
        '''
        Subscribe to events.
        '''
        self._event_bus.subscribe("panel_order_changed", self._on_panel_order_changed)

    def _setup_ui(self) -> None:
        '''
        Setup the UI components of the panel container.
        '''
        panels_settings = self._settings.get("panels")
        width = panels_settings.get("width", 300)
        self.configure(width=width)

        for panel_name in panels_settings.get("enabled"):
            PanelRegistry.register_panel(panel_name)
            panel_class = PanelRegistry.get_panel(panel_name)
            if panel_class:
                panel_instance = panel_class(self, self._event_bus)
                panel_instance.pack(fill=ctk.X, padx=5, pady=5)

    def _on_panel_order_changed(self, data: dict = None) -> None:
        '''
        Handle changes in panel order.
        
        :param data: Datas from event_bus.
        :type data: dict, optional
        '''
        pass
