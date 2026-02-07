import customtkinter as ctk
from controllers import EventBus
from models import (
    SettingsManager, 
    IconManager,
)
from views.top_bar import TopBar
from views.workspace import Workspace

class MainWindow(ctk.CTk):
    '''
    Main Application Class.

    :param event_bus: The global event_bus to communicate with others scripts.
    :type event_bus: EventBus
    :param settings: The global settings manager to access settings from nowhere.
    :type settings: SettingsManager
    :param icons: The global icons manager to access icons from nowhere.
    :type icons: IconManager
    '''
    def __init__(self, event_bus: EventBus, settings: SettingsManager, icons: IconManager) -> None:
        super().__init__()

        self._event_bus = event_bus
        self._settings = settings
        self._icons = icons

        self._top_bar = TopBar(self, event_bus, settings, icons)
        self._workspace = Workspace(self, event_bus, settings)

        self.title("Photo Editor")
        self._setup_ui()
        self._setup_bindings()
        self.after(100, self._load_settings)

    def _setup_ui(self) -> None:
        '''
        Setup UI components.
        '''
        settings = self._settings.get_all()
        ctk.set_appearance_mode(settings.appearance)
        ctk.set_default_color_theme(settings.color_theme)
        
        if settings.geometry:
            self.geometry(settings.geometry)
        else:
            self.geometry("800x600")

        self._top_bar.pack(fill=ctk.X, padx=5, pady=(5, 0))
        self._workspace.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

    def _setup_bindings(self) -> None:
        '''
        Setup event bindings.
        '''
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.bind("<F11>", self._toggle_fullscreen())
        self.bind_all("<Button-1>", lambda e: e.widget.focus_set())

    def _load_settings(self) -> None:
        '''
        Load settings.
        '''
        if self._settings.get("fullscreen"): self.state("zoomed")

    def _on_closing(self) -> None:
        '''
        Save settings and close the app.
        '''
        if self.state() == 'zoomed':
            self._settings.set("fullscreen", True)
            self._settings.set("geometry", None)
        else:
            self._settings.set("fullscreen", False)
            self._settings.set("geometry", self.geometry())
        
        self._settings.save()
        self.destroy()

    def _toggle_fullscreen(self) -> None:
        '''
        Toggle fullscreen.
        '''
        self.state('zoomed') if self.state() == 'normal' else self.state('normal')
