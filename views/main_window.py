import customtkinter as ctk
from controllers.event_bus import EventBus
from models.settings import SettingsManager
from views.top_bar import TopBar
from views.workspace import Workspace

class MainWindow(ctk.CTk):
    ''' Main Application Class. '''

    def __init__(self, event_bus: EventBus, settings: SettingsManager):
        super().__init__()

        self.event_bus = event_bus
        self.settings = settings

        # Window configuration
        self.title("Photo Editor")
        self._setup_ui()

        self.top_bar = TopBar(self, event_bus)
        self.workspace = Workspace(self, event_bus, settings)

        self.top_bar.pack(fill=ctk.X, padx=5, pady=(5, 0))
        self.workspace.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

        self._setup_bindings()
        
        self.after(100, self._load_settings)

    def _setup_ui(self):
        ''' Setup the UI components. '''
        settings = self.settings.get_all()
        ctk.set_appearance_mode(settings.appearance)
        ctk.set_default_color_theme(settings.color_theme)
        
        if settings.geometry:
            self.geometry(settings.geometry)
        else:
            self.geometry("800x600")
    
    def _setup_bindings(self):
        ''' Setup event bindings. '''
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.bind("<F11>", lambda e: self._toggle_fullscreen())
        self.bind_all("<Button-1>", lambda e: e.widget.focus_set())
        
    def _load_settings(self):
        ''' Load settings from the settings.json file. '''
        if self.settings.get("fullscreen"): 
            self.state("zoomed")
    
    def _on_closing(self):
        ''' Save settings and close the app. '''
        # Save window state/geometry
        if self.state() == 'zoomed':
            self.settings.set("fullscreen", True)
            self.settings.set("geometry", None)
        else:
            self.settings.set("fullscreen", False)
            self.settings.set("geometry", self.geometry())
        
        self.settings.save()
        self.destroy()

    def _toggle_fullscreen(self):
        ''' Toggle fullscreen mode. '''
        if self.state() == 'normal':
            self.state('zoomed')
        else:
            self.state('normal')
