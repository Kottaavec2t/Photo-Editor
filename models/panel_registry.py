from dataclasses import dataclass
from views.panels.edit_panel import EditPanel
from views.panels.history_panel import HistoryPanel

_panels = {
    "edit": EditPanel,
    "history": HistoryPanel
}

class PanelRegistry:
    ''' Registry for all available panels in the application. '''
    _registry = {}

    @classmethod
    def register_panel(cls, panel_name: str):
        ''' Register a new panel class with a given name. '''
        if panel_name in _panels:
            cls._registry[panel_name] = _panels.get(panel_name)

    @classmethod
    def get_panel(cls, panel_name: str):
        ''' Retrieve a panel class by its name. '''
        return cls._registry.get(panel_name)

    @classmethod
    def get_all_panels(cls):
        ''' Retrieve all registered panel classes. '''
        return cls._registry