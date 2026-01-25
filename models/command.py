"""Command Pattern implementation for undo/redo system."""
from abc import ABC, abstractmethod
from PIL import Image
from typing import Optional, List


class Command(ABC):
    """Abstract base class for all commands."""
    
    @abstractmethod
    def execute(self, image: Image.Image) -> Image.Image:
        """Execute the command and return the modified image."""
        pass
    
    @abstractmethod
    def undo(self, image: Image.Image) -> Image.Image:
        """Undo the command and return the previous image."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get a human-readable description of the command."""
        pass


class CommandGroup(Command):
    """Groups multiple commands into a single transaction/folder."""
    
    def __init__(self, description: str = "Transaction"):
        self.commands: List[Command] = []
        self._description = description
    
    def add_command(self, command: Command):
        """Add a command to this group."""
        self.commands.append(command)
    
    def execute(self, image: Image.Image) -> Image.Image:
        """Execute all commands in the group sequentially."""
        current_image = image.copy()
        for command in self.commands:
            current_image = command.execute(current_image)
        return current_image
    
    def undo(self, image: Image.Image) -> Image.Image:
        """Undo all commands in reverse order."""
        current_image = image.copy()
        # Execute all commands in reverse order to get back to original state
        for command in reversed(self.commands):
            current_image = command.undo(current_image)
        return current_image
    
    def get_description(self) -> str:
        """Get the group description."""
        return self._description
    
    def is_empty(self) -> bool:
        """Check if the group has any commands."""
        return len(self.commands) == 0


class BrightnessCommand(Command):
    """Command for adjusting brightness."""
    
    def __init__(self, factor: float, original_image: Image.Image = None):
        self.factor = factor
        # Store the original image state in case we need it for undo
        self.original_image = original_image.copy() if original_image else None
    
    def execute(self, image: Image.Image) -> Image.Image:
        """Apply brightness adjustment."""
        from utils.image_operations import brightness
        return brightness(image, self.factor)
    
    def undo(self, image: Image.Image) -> Image.Image:
        """Undo brightness adjustment by applying inverse factor."""
        from utils.image_operations import brightness
        if self.factor != 0:
            inverse_factor = 1.0 / self.factor
            return brightness(image, inverse_factor)
        return image
    
    def get_description(self) -> str:
        """Get command description."""
        return f"Brightness ({self.factor:.2f}x)"


class RotationCommand(Command):
    """Command for rotating image."""
    
    def __init__(self, angle: float, original_image: Image.Image = None):
        self.angle = angle
        # Store the original image state in case we need it for undo
        self.original_image = original_image.copy() if original_image else None
    
    def execute(self, image: Image.Image) -> Image.Image:
        """Apply rotation."""
        from utils.image_operations import rotate
        return rotate(image, self.angle)
    
    def undo(self, image: Image.Image) -> Image.Image:
        """Undo rotation by rotating in opposite direction."""
        from utils.image_operations import rotate
        return rotate(image, -self.angle)
    
    def get_description(self) -> str:
        """Get command description."""
        return f"Rotation ({self.angle:.1f}°)"


class GrayscaleCommand(Command):
    """Command for converting to grayscale."""
    
    def __init__(self, original_image: Image.Image = None):
        self.original_image = original_image.copy() if original_image else None
    
    def execute(self, image: Image.Image) -> Image.Image:
        """Convert to grayscale."""
        from utils.image_operations import black_and_white
        return black_and_white(image)
    
    def undo(self, image: Image.Image) -> Image.Image:
        """Undo grayscale by reverting to original color image."""
        if self.original_image:
            return self.original_image.copy()
        return image
    
    def get_description(self) -> str:
        """Get command description."""
        return "Grayscale"


class CropCommand(Command):
    """Command for cropping image."""
    
    def __init__(self, box: tuple, original_image: Image.Image = None):
        self.box = box  # (left, top, right, bottom)
        self.original_image = original_image.copy() if original_image else None
    
    def execute(self, image: Image.Image) -> Image.Image:
        """Apply crop."""
        from utils.image_operations import crop
        return crop(image, self.box)
    
    def undo(self, image: Image.Image) -> Image.Image:
        """Undo crop by reverting to original."""
        if self.original_image:
            return self.original_image.copy()
        return image
    
    def get_description(self) -> str:
        """Get command description."""
        left, top, right, bottom = self.box
        return f"Crop ({right-left}x{bottom-top})"


class ResizeCommand(Command):
    """Command for resizing image."""
    
    def __init__(self, new_size: tuple, original_image: Image.Image = None):
        self.new_size = new_size
        # Store the original image state for undo
        self.original_image = original_image.copy() if original_image else None
    
    def execute(self, image: Image.Image) -> Image.Image:
        """Apply resize."""
        from utils.image_operations import resize
        return resize(image, self.new_size)
    
    def undo(self, image: Image.Image) -> Image.Image:
        """Undo resize by reverting to original."""
        if self.original_image:
            return self.original_image.copy()
        return image
    
    def get_description(self) -> str:
        """Get command description."""
        return f"Resize ({self.new_size[0]}x{self.new_size[1]})"


class CustomCommand(Command):
    """Generic command that takes a function."""
    
    def __init__(self, execute_func, undo_func, description: str):
        self.execute_func = execute_func
        self.undo_func = undo_func
        self._description = description
    
    def execute(self, image: Image.Image) -> Image.Image:
        """Execute the custom function."""
        return self.execute_func(image)
    
    def undo(self, image: Image.Image) -> Image.Image:
        """Undo using the custom undo function."""
        return self.undo_func(image)
    
    def get_description(self) -> str:
        """Get command description."""
        return self._description
