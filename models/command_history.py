"""Command history manager for tracking undo/redo operations."""
from models.command import Command, CommandGroup
from PIL import Image
from typing import List, Optional, Dict


class CommandHistory:
    """Manages command history with undo/redo and grouping support.
    
    NEW FEATURE: Intelligent command replacement
    When a new command of the same type is executed, it replaces the previous
    one at the top of the undo stack, while keeping the old command in the
    undo history for potential recovery.
    """
    
    def __init__(self, max_history: int = 100, smart_replace: bool = True):
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []
        self._current_group: Optional[CommandGroup] = None
        self._max_history = max_history
        self._smart_replace = smart_replace  # Enable/disable smart replacement
        self._replaced_commands: Dict[str, List[Command]] = {}  # Track replaced commands by type
    
    def begin_group(self, description: str = "Transaction"):
        """Start a group of commands that will be undone/redone together."""
        if self._current_group is not None:
            raise RuntimeError("Cannot nest command groups. End the current group first.")
        self._current_group = CommandGroup(description)
    
    def end_group(self):
        """End the current command group and add it to history if non-empty."""
        if self._current_group is None:
            raise RuntimeError("No group is currently open.")
        
        if not self._current_group.is_empty():
            self._undo_stack.append(self._current_group)
            self._redo_stack.clear()
            self._trim_history()
        
        self._current_group = None
    
    def execute_command(self, command: Command, image: Image.Image) -> Image.Image:
        """
        Execute a command and add it to the history.
        If smart_replace is enabled and the last command has the same type,
        the last command is moved to replaced history and the new one takes its place.
        
        If a group is open, add the command to the group instead of history.
        """
        result = command.execute(image)
        
        if self._current_group is not None:
            self._current_group.add_command(command)
        else:
            # Smart replacement: if last command is same type, replace it
            if self._smart_replace and self._should_replace(command):
                replaced = self._undo_stack.pop()
                command_type = type(replaced).__name__
                
                # Store the replaced command in history
                if command_type not in self._replaced_commands:
                    self._replaced_commands[command_type] = []
                self._replaced_commands[command_type].append(replaced)
            
            self._undo_stack.append(command)
            self._redo_stack.clear()
            self._trim_history()
        
        return result
    
    def undo(self, image: Image.Image) -> Optional[Image.Image]:
        """
        Undo the last command or group and return the resulting image.
        Returns None if there's nothing to undo.
        """
        if not self.can_undo():
            return None
        
        command = self._undo_stack.pop()
        self._redo_stack.append(command)
        
        # Rebuild the image state by re-executing all remaining undo stack commands
        current_image = image.copy()
        for cmd in self._undo_stack:
            current_image = cmd.execute(current_image)
        
        return current_image
    
    def redo(self, image: Image.Image) -> Optional[Image.Image]:
        """
        Redo the last undone command or group and return the resulting image.
        Returns None if there's nothing to redo.
        """
        if not self.can_redo():
            return None
        
        command = self._redo_stack.pop()
        self._undo_stack.append(command)
        
        # Rebuild the image state by re-executing all undo stack commands
        current_image = image.copy()
        for cmd in self._undo_stack:
            current_image = cmd.execute(current_image)
        
        return current_image
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0
    
    def get_undo_description(self) -> Optional[str]:
        """Get description of the next undo action."""
        if not self.can_undo():
            return None
        return self._undo_stack[-1].get_description()
    
    def get_redo_description(self) -> Optional[str]:
        """Get description of the next redo action."""
        if not self.can_redo():
            return None
        return self._redo_stack[-1].get_description()
    
    def get_history(self) -> List[str]:
        """Get list of command descriptions in history (for debugging/UI)."""
        return [cmd.get_description() for cmd in self._undo_stack]
    
    def get_future(self) -> List[str]:
        """Get list of command descriptions in redo stack (for debugging/UI)."""
        return [cmd.get_description() for cmd in self._redo_stack]
    
    def clear(self):
        """Clear all history."""
        self._undo_stack.clear()
        self._redo_stack.clear()
        if self._current_group is not None:
            self._current_group = None
    
    def _trim_history(self):
        """Remove oldest commands if history exceeds max size."""
        if len(self._undo_stack) > self._max_history:
            self._undo_stack = self._undo_stack[-self._max_history:]
    
    def has_active_group(self) -> bool:
        """Check if there's currently an open command group."""
        return self._current_group is not None
    
    def _should_replace(self, command: Command) -> bool:
        """Check if the new command should replace a previous one of the same type.
        
        Searches for the most recent command of the same type, regardless of
        what commands are in between.
        """
        if not self._undo_stack:
            return False
        
        command_type = type(command).__name__
        
        # Search backwards through the stack for a command of the same type
        for i in range(len(self._undo_stack) - 1, -1, -1):
            existing_cmd = self._undo_stack[i]
            
            # Skip command groups
            if isinstance(existing_cmd, CommandGroup):
                continue
            
            # Found a command of the same type - we should replace it
            if type(existing_cmd).__name__ == command_type:
                return True
        
        # No command of the same type found
        return False
    
    def get_replaced_commands(self, command_type: str) -> List[Command]:
        """Get list of replaced commands for a given type."""
        return self._replaced_commands.get(command_type, [])
    
    def clear_replaced_commands(self, command_type: Optional[str] = None):
        """Clear replaced commands. If command_type is None, clear all."""
        if command_type is None:
            self._replaced_commands.clear()
        elif command_type in self._replaced_commands:
            del self._replaced_commands[command_type]
