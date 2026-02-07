import customtkinter as ctk
from views.photo_viewer import PhotoViewer 
from views.panel_container import PanelContainer
from controllers import EventBus
from models import SettingsManager

class Workspace(ctk.CTkFrame):
    '''
    Main workspace area for editing photos.

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
        self._event_bus.subscribe("panel_configuration_changed", self._on_panel_configuration_changed)

    def _setup_ui(self) -> None:
        '''
        Setup the UI components of the workspace.
        '''
        self.photo_frame = PhotoViewer(self, self._event_bus)
        self.panel_container = PanelContainer(self, self._event_bus, self._settings)

        panels_settings = self._settings.get("panels")

        if panels_settings and panels_settings.get("position") == "right":
            self.panel_container.pack(side=ctk.RIGHT, fill=ctk.Y)
            self.photo_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        else:
            self.panel_container.pack(side=ctk.LEFT, fill=ctk.Y)
            self.photo_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

    def _on_panel_configuration_changed(self, data: dict = None) -> None:
        '''
        Handle changes in panel configuration.
        
        :param data: Datas from event_bus.
        :type data: dict, optional
        '''
        if data['panels'].get("position") == "right":
            self.panel_container.pack(side=ctk.RIGHT, fill=ctk.Y)
            self.photo_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        else:
            self.panel_container.pack(side=ctk.LEFT, fill=ctk.Y)
            self.photo_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)
