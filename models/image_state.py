'''Module for managing image state with history.'''

from PIL import Image
from typing import Callable

class ImageStateManager:
    '''Controller class to manage image operations with undo/redo functionality.'''
    def __init__(self):
        self._current_image: Image.Image | None = None
        self._history: list[Image.Image] = []
        self._future: list[Image.Image] = []

    def load_image(self, fp: str):
        '''Loads a new image and resets history.'''
        self._current_image = Image.open(fp)
        self._history.clear()
        self._future.clear()

    def get_current_image(self) -> Image.Image | None:
        '''Returns the current image.'''
        if self._current_image is not None:
            return self._current_image.copy()
        return None

    def apply_operation(self, operation_func: Callable, *args, **kwargs):
        '''Applies an image operation and manages history for undo/redo.
        :param operation_func: (Callable) A function that takes an Image and returns a modified Image.
        :param *args: Positional arguments for the operation function.
        :param **kwargs: Keyword arguments for the operation function.
        :return: None
        '''
        if self._current_image is not None:
            self._history.append(self._current_image.copy())
            self._current_image = operation_func(self._current_image, *args, **kwargs)
            self._future.clear()
    
    def undo(self):
        '''Reverts to the previous image state if available.'''
        if self._history:
            self._future.append(self._current_image.copy())
            self._current_image = self._history.pop()
    
    def redo(self):
        '''Reapplies the last undone image state if available.'''
        if self._future:
            self._history.append(self._current_image.copy())
            self._current_image = self._future.pop()

    def can_undo(self) -> bool:
        '''Checks if undo is possible.'''
        return len(self._history) > 0
    
    def can_redo(self) -> bool:
        '''Checks if redo is possible.'''
        return len(self._future) > 0