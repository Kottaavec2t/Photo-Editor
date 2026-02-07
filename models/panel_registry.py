from views.panels import (
    EditPanel, 
    HistoryPanel,
)

_panels = {
    "edit": EditPanel,
    "history": HistoryPanel
}

class PanelRegistry:
    '''
    Registry for all available panels in the application.
    '''
    _registry = {}

    @classmethod
    def register_panel(cls, panel_name: str) -> None:
        '''
        Register a new panel class with a given name.

        :param panel_name: The name of the panel.
        '''
        if panel_name in _panels:
            cls._registry[panel_name] = _panels.get(panel_name)

    @classmethod
    def get_panel(cls, panel_name: str) -> None:
        '''
        Retrieve a panel class by its name.

        :param panel_name: The name of the panel.
        '''
        return cls._registry.get(panel_name)

    @classmethod
    def get_all_panels(cls) -> dict:
        '''
        Retrieve all registered panel classes.

        :return: All the registered pannels.
        :rtype: dict
        '''
        return cls._registry
