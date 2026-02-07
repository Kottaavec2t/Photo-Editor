import json
import os
from typing import Any, Optional
from dataclasses import dataclass, asdict, field

@dataclass
class AppSettings:
    '''
    App settings framework.
    '''
    appearance: str = "Light"
    color_theme: str = "green"
    geometry: Optional[str] = None
    fullscreen: bool = False
    panels: dict = field(default_factory=lambda: dict({
        "position": "right",
        "width": 500,
        "enabled": ["edit"]
    }))

class SettingsManager:
    '''
    Manage settings saving and loading.

    :param filepath: The path to the settings file.
    :type filepath: str, optional 
    '''
    def __init__(self, filepath: str = "settings.json") -> None:
        self._filepath = filepath
        self._settings = self._load()
        print(f"Paramètres chargés : {self._settings}")

    def _load(self) -> AppSettings:
        '''
        Load settings with JSON file.

        :return: The settings framework initialized.
        :rtype: AppSettings
        '''
        if not os.path.exists(self._filepath): return AppSettings()
        
        try:
            with open(self._filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return AppSettings(**data)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Erreur lors du chargement des paramètres: {e}")
            return AppSettings()

    def save(self) -> None:
        '''
        Save settings in JSON file.
        '''
        try:
            with open(self._filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._settings), f, indent=4)
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des paramètres: {e}")

    def get(self, key: str) -> Any | None:
        '''
        Collect a settings value.

        :param key: The setting name.
        :type key: str
        :return: The wanted settings.
        :rtype: any | None
        '''
        return getattr(self._settings, key, None)

    def set(self, key: str, value: Any) -> None:
        '''
        Set a settings value.

        :param key: The name of the setting.
        :type key: str
        :param value: The value to set.
        :type value: any
        '''
        if hasattr(self._settings, key):
            setattr(self._settings, key, value)

    def get_all(self) -> AppSettings:
        '''
        Collect all settings.

        :return: Settings framework initialized.
        :rtype: AppSettings
        '''
        return self._settings
