import customtkinter as ctk
from views.photo_viewer import PhotoViewer
from views.panel_container import PanelContainer

class Workspace(ctk.CTkFrame):
    ''' Main workspace area for editing photos. '''

    def __init__(self, master, event_bus, settings):
        super().__init__(master)

        self.event_bus = event_bus
        self.settings = settings

        self._setup_ui()
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        ''' Setup event subscriptions. '''
        
        self.event_bus.subscribe("panel_configuration_changed", self._on_panel_configuration_changed)

    def _setup_ui(self):
        ''' Setup the UI components of the workspace. '''
        
        self.photo_frame = PhotoViewer(self, self.event_bus)
        self.panel_container = PanelContainer(self, self.event_bus, self.settings)

        panels_settings = self.settings.get("panels")

        if panels_settings and panels_settings.get("position") == "right":
            self.panel_container.pack(side=ctk.RIGHT, fill=ctk.Y)
            self.photo_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

    def _on_panel_configuration_changed(self, data: dict = None):
        ''' Handle changes in panel configuration. '''
        
        if data['panels'].get("position") == "right":
            self.panel_container.pack(side=ctk.RIGHT, fill=ctk.Y)
            self.photo_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        else:
            self.panel_container.pack(side=ctk.LEFT, fill=ctk.Y)
            self.photo_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)
        