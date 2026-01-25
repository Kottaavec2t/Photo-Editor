'''Module for managing image state with history using Command Pattern.'''

from PIL import Image
from models.command_history import CommandHistory
from models.command import Command


class ImageStateManager:
    '''
    Manages image state with undo/redo using Command Pattern.
    
    This implementation allows:
    - Individual commands to be undone/redone separately
    - Grouping commands into transactions that undo/redo as a unit
    - Flexible command architecture for custom operations
    '''
    
    def __init__(self, max_history: int = 100):
        self._base_image: Image.Image | None = None
        self._current_image: Image.Image | None = None
        self._command_history = CommandHistory(max_history)
    
    def load_image(self, fp: str):
        '''Loads a new image and resets history.'''
        image = Image.open(fp)
        self._base_image = image.copy()
        self._current_image = image.copy()
        self._command_history.clear()
    
    def get_current_image(self) -> Image.Image | None:
        '''Returns the current image.'''
        if self._current_image is not None:
            return self._current_image.copy()
        return None
    
    def execute_command(self, command: Command) -> Image.Image | None:
        '''
        Execute a command and add it to history.
        
        If a group is open (via begin_transaction), the command is added to the group.
        Otherwise, the command is executed immediately and added to history.
        
        :param command: The Command to execute
        :return: The resulting image after command execution, or None if no image is loaded
        '''
        if self._current_image is None:
            return None
        
        # Add command to history
        self._command_history.execute_command(command, self._base_image)
        
        # Rebuild the image by applying ALL commands in order from base image
        self._current_image = self._base_image.copy()
        for cmd in self._command_history._undo_stack:
            self._current_image = cmd.execute(self._current_image)
        
        return self._current_image.copy()
    
    def begin_transaction(self, description: str = "Transaction"):
        '''
        Begin a group of commands that will be undone/redone together.
        
        Example:
            image_state.begin_transaction("Adjust brightness and rotation")
            image_state.execute_command(BrightnessCommand(...))
            image_state.execute_command(RotationCommand(...))
            image_state.end_transaction()
        '''
        self._command_history.begin_group(description)
    
    def end_transaction(self):
        '''End the current transaction/group.'''
        self._command_history.end_group()
    
    def undo(self) -> Image.Image | None:
        '''
        Undo the last command or transaction.
        
        :return: The resulting image, or None if nothing to undo
        '''
        result = self._command_history.undo(self._base_image)
        if result is not None:
            self._current_image = result
            return self._current_image.copy()
        return None
    
    def redo(self) -> Image.Image | None:
        '''
        Redo the last undone command or transaction.
        
        :return: The resulting image, or None if nothing to redo
        '''
        result = self._command_history.redo(self._base_image)
        if result is not None:
            self._current_image = result
            return self._current_image.copy()
        return None
    
    def can_undo(self) -> bool:
        '''Checks if undo is possible.'''
        return self._command_history.can_undo()
    
    def can_redo(self) -> bool:
        '''Checks if redo is possible.'''
        return self._command_history.can_redo()
    
    def get_undo_description(self) -> str | None:
        '''Get description of the next undo action.'''
        return self._command_history.get_undo_description()
    
    def get_redo_description(self) -> str | None:
        '''Get description of the next redo action.'''
        return self._command_history.get_redo_description()
    
    def get_history(self) -> list[str]:
        '''Get list of command descriptions in history (for UI display).'''
        return self._command_history.get_history()
    
    def clear_history(self):
        '''Clear all undo/redo history (e.g., when starting a new edit session).'''
        self._command_history.clear()
    
    def has_active_transaction(self) -> bool:
        '''Check if there's an open transaction/group.'''
        return self._command_history.has_active_group()