"""Gestion des paramètres de l'application."""

import json
import os
from typing import Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class AppSettings:
    """Structure des paramètres de l'application."""
    appearance: str = "Dark"
    color_theme: str = "green"
    geometry: Optional[str] = None
    fullscreen: bool = False
    last_directory: str = ""
    max_history: int = 50
    auto_save: bool = False

class SettingsManager:
    """Gère le chargement et la sauvegarde des paramètres."""
    
    def __init__(self, filepath: str = "settings.json"):
        self._filepath = filepath
        self._settings = self._load()
    
    def _load(self) -> AppSettings:
        """Charge les paramètres depuis le fichier JSON."""
        if not os.path.exists(self._filepath):
            return AppSettings()
        
        try:
            with open(self._filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return AppSettings(**data)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Erreur lors du chargement des paramètres: {e}")
            return AppSettings()
    
    def save(self):
        """Sauvegarde les paramètres dans le fichier JSON."""
        try:
            with open(self._filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._settings), f, indent=4)
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des paramètres: {e}")
    
    def get(self, key: str) -> Any:
        """Récupère une valeur de paramètre."""
        return getattr(self._settings, key, None)
    
    def set(self, key: str, value: Any):
        """Définit une valeur de paramètre."""
        if hasattr(self._settings, key):
            setattr(self._settings, key, value)
    
    def get_all(self) -> AppSettings:
        """Retourne tous les paramètres."""
        return self._settings