'''Gestion des icones de l'application'''

import os
from typing import Any, Optional
from dataclasses import dataclass, asdict, field
from PIL import Image, ImageTk
import customtkinter as ctk
from utils.text_operations import remove_file_extension

class IconManager:
    def __init__(self, filepath: str = 'images'):
        self._filepath = filepath
        self._icons = {} # {'name': Icon}

        self._load()

    def _load(self):
        '''
        Load the images to the _icons table.
        '''
        self._dark_fp = os.path.join(self._filepath, "dark")
        self._light_fp = os.path.join(self._filepath, "light")
        icon_dir = [f for f in os.listdir(self._dark_fp) if os.path.isfile(os.path.join(self._dark_fp, f))]
        for img in icon_dir:
            dark_path = os.path.join(self._dark_fp, img) # dark icon
            light_path = os.path.join(self._light_fp, img) # light icon
            print(f"Loading icon: {img}")
            name = remove_file_extension(img, '.png') # remove the .png extension
            self._icons[name] = ctk.CTkImage(Image.open(light_path), Image.open(dark_path))

    def get(self, name: str) -> ctk.CTkImage | None:
        '''
        Get an icon by name
        
        :param name: the name of the wanted icon
        :type name: str
        :return: the icon or None if not found
        :rtype: CTkImage | None
        '''
        return self._icons.get(name, None)