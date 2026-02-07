from PIL import Image
from typing import List
from models import CommandHistory
from models.commands import Command

class ImageStateManager:
    '''
    Manages image state.
    Undo/redo using Command Pattern.

    :param max_history: Max history limit. Adjust on machine performance.
    :type max_history: int, optional
    '''
    def __init__(self, max_history: int = 100):
        self._base_image: Image.Image | None = None
        self._current_image: Image.Image | None = None
        self._command_history = CommandHistory(max_history)

    def load_image(self, fp: str) -> None:
        '''
        Loads a new image and resets history.

        :param fp: The file path of the image to load.
        :type fp: str
        '''
        image = Image.open(fp)
        self._base_image = image.copy()
        self._current_image = image.copy()
        self._command_history.clear_history()

    def get_current_image(self) -> Image.Image | None:
        '''
        Returns the current image.

        :return: The current image, or None if no image is loaded.
        :rtype: Image.Image | None
        '''
        if self._current_image is not None:
            return self._current_image.copy()
        return None

    def execute_command(self, command: Command, save_in_history: bool = True) -> Image.Image | None:
        '''
        Execute a command.
        If save_in_history is True then command is saved in history.

        :param command: The Command to execute.
        :type command: Command
        :param save_in_history: True if the command is save in the history else False.
        :type save_in_history: bool, optional
        :return: The resulting image after command execution, or None if no image is loaded.
        :rtype: Image.Image | None
        '''
        if self._current_image is None: return None
        if save_in_history: self._command_history.add_command(command) # Add command to history if save_in_history
        if not self._command_history._command_type_in_history(command): return command.execute(self._current_image) # if the command type is not in history execute it directly

        modified_image = self._rebuild_image(command if not save_in_history else None)
        if not save_in_history: modified_image = command.execute(modified_image) # add the new command

        self._current_image = modified_image # stock the new image

        return modified_image

    def undo(self) -> Image.Image | None:
        '''
        Undo the last command or transaction.

        :return: The resulting image, or None if nothing to undo.
        :rtype: Image.Image | None
        '''
        self._command_history.undo()
        new_image = self._rebuild_image()
        if new_image is not None:
            self._current_image = new_image
            return self._current_image.copy()
        return None

    def redo(self) -> Image.Image | None:
        '''
        Redo the last undone command or transaction.

        :return: The resulting image, or None if nothing to redo.
        :rtype: Image.Image | None
        '''
        self._command_history.redo()
        new_image = self._rebuild_image()
        if new_image is not None:
            self._current_image = new_image
            return self._current_image.copy()
        return None

    def can_undo(self) -> bool:
        '''
        Determine if the undo is possible.

        :return: True if the undo_stack is not empty else False.
        :rtype: bool
        '''
        return self._command_history.can_undo()

    def can_redo(self) -> bool:
        '''
        Determine if the redo is possible.

        :return: True if the redo_stack is not empty else False.
        :rtype: bool
        '''
        return self._command_history.can_redo()

    def get_undo_stack(self) -> List[Command]:
        '''
        Return the undo stack.

        :return: A list of commands.
        :rtype: List[Command]
        '''
        return self._command_history.get_undo_stack()

    def get_redo_stack(self) -> List[Command]:
        '''
        Return the redo stack.

        :return: A list of commands.
        :rtype: List[Command]
        '''
        return self._command_history.get_redo_stack()

    def clear_history(self) -> None:
        '''
        Clear all history.
        '''
        self._command_history.clear_history()

    def _rebuild_image(self, pass_command: Command = None) -> Image.Image:
        '''
        Recalculate the image modifications with the command history.
        Take a command to be passed in case not save_in_history.

        :param pass_command: The skipped type command.
        :type pass_command: Command, optional
        :return: The rebuilt image.
        :rtype: Image.Image
        '''
        seen = set() # all command type already seen
        if pass_command is not None: seen.add(type(pass_command).__name__) # add the new command type to seen to not execute it twice if it's not in history
        retained = [] # all command to execute to rebuild the image
        undo_stack = self._command_history.get_undo_stack() # command history

        # sort all commands in the history to get only one of every type
        for current_command in reversed(undo_stack):
            current_command_type = type(current_command).__name__
            if current_command_type not in seen:
                seen.add(current_command_type) # add the type to seen
                retained.append(current_command) # add the command to retained

        modified_image = self._base_image.copy()

        # inverse order = chronological order
        for current_command in reversed(retained):
            modified_image = current_command.execute(modified_image)

        return modified_image
