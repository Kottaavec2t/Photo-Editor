from typing import List
from models.commands import Command

class CommandHistory:
    '''
    Handle Command Pattern history.

    :param max_history: Max history limit. Adjust on machine performance.
    :type max_history: int, optional
    '''
    def __init__(self, max_history: int = 100) -> None:
        self._max_history = max_history
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []

    def add_command(self, command: Command) -> None:
        '''
        Add a command to the history.
        
        :param command: The command to add.
        :type command: Command
        '''
        self._undo_stack.append(command)
        self._redo_stack.clear()
        self._trim_history()

    def undo(self) -> None:
        '''
        Undo last command.
        '''
        if not self.can_undo(): return None
        command = self._undo_stack.pop()
        self._redo_stack.append(command)
        return command

    def redo(self) -> None:
        '''
        Redo last command.
        '''
        if not self.can_redo(): return None
        command = self._redo_stack.pop()
        self._undo_stack.append(command)
        return command

    def can_undo(self) -> bool:
        '''
        Determine if the undo is possible.
        
        :return: True if the undo_stack is not empty else False.
        :rtype: bool
        '''
        return not self._undo_stack == []

    def can_redo(self) -> bool:
        '''
        Determine if the redo is possible.
        
        :return: True if the redo_stack is not empty else False.
        :rtype: bool
        '''
        return not self._redo_stack == []

    def get_undo_stack(self)-> List[Command]:
        '''
        Return the undo stack.

        :return: A list of commands.
        :rtype: List[Command]
        '''
        return self._undo_stack

    def get_redo_stack(self) -> List[Command]:
        '''
        Return the redo stack.

        :return: A list of commands.
        :rtype: List[Command]
        '''
        return self._redo_stack

    def clear_history(self) -> None:
        '''
        Clear all history.
        '''
        self._undo_stack = []
        self._redo_stack = []

    def _trim_history(self) -> None:
        '''
        Remove oldest commands if history exceeds max size.
        '''
        if len(self._undo_stack) > self._max_history:
            self._undo_stack = self._undo_stack[-self._max_history:]

    def _command_type_in_history(self, command: Command) -> bool:
        '''
        Tells if the command is in the history.
        
        :param command: The command to check.
        :type command: Command
        :return: True if the command is in the history else False.
        :rtype: bool
        '''
        command_type = type(command).__name__
        for cmd in self._undo_stack:
            if type(cmd).__name__ == command_type:
                return True
        return False
