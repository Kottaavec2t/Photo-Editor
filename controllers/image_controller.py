"""Contrôleur principal pour les opérations sur l'image."""
from controllers.event_bus import EventBus
from models.image_state import ImageStateManager
from models.command import (
    BrightnessCommand,
    RotationCommand,
    GrayscaleCommand,
    CropCommand,
    ResizeCommand,
)
import utils.image_operations as img_op
from customtkinter import filedialog
from tkinter import messagebox

class ImageController:
    """Handle image operations and communicate with the event bus."""
    
    def __init__(self, event_bus: EventBus, image_state: ImageStateManager):
        self.event_bus = event_bus
        self.image_state = image_state
        
        # Subscribing to events
        self._subscribe_to_events()
    
    def _subscribe_to_events(self):
        """Subscribe to event bus events."""
        self.event_bus.subscribe("import_requested", self._handle_import)
        self.event_bus.subscribe("save_requested", self._handle_save)
        self.event_bus.subscribe("undo_requested", self._handle_undo)
        self.event_bus.subscribe("redo_requested", self._handle_redo)
        self.event_bus.subscribe("image_operation_applied", self._handle_operation)
    
    def _handle_import(self, data: dict = None):
        """Handle image import."""
        filetypes = [
            ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=filetypes
        )
        
        if not filepath:
            return
        
        try:
            self.image_state.load_image(filepath)
            image = self.image_state.get_current_image()
            print(image)
            self.event_bus.publish("image_loaded", {'image': image})
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load image: {e}")
    
    def _handle_save(self, data: dict = None):
        """Handle image saving."""
        current_image = self.image_state.get_current_image()
        
        if current_image is None:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        filetypes = [
            ("PNG", "*.png"),
            ("JPEG", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            filetypes=filetypes
        )
        
        if not filepath:
            return
        
        try:
            current_image.save(filepath)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to save image: {e}")
    
    def _handle_undo(self, data: dict = None):
        """Handle undo."""
        image = self.image_state.undo()
        
        if image:
            self.event_bus.publish("image_modified", {'image': image})
            # Notify that redo is available
            self.event_bus.publish("redo_available", {'available': self.image_state.can_redo()})
            # Notify that undo availability changed
            self.event_bus.publish("undo_available", {'available': self.image_state.can_undo()})
        else:
            messagebox.showinfo("Info", "Nothing to undo")
    
    def _handle_redo(self, data: dict = None):
        """Handle redo."""
        image = self.image_state.redo()
        
        if image:
            self.event_bus.publish("image_modified", {'image': image})
            # Notify that undo is available
            self.event_bus.publish("undo_available", {'available': self.image_state.can_undo()})
            # Notify that redo availability changed
            self.event_bus.publish("redo_available", {'available': self.image_state.can_redo()})
        else:
            messagebox.showinfo("Info", "Nothing to redo")
    
    def _handle_operation(self, data: dict = None):
        """Apply an operation on the image."""
        try:
            current_image = self.image_state.get_current_image()
            if current_image is None or data is None:
                return
            
            # Determine the operation type if provided
            operation_type = data.get('operation_type', 'custom')
            description = data.get('description', 'Custom Operation')
            
            # Create appropriate command based on type
            if operation_type == 'brightness':
                factor = data.get('value', 1.0)
                command = BrightnessCommand(factor, current_image)
            elif operation_type == 'rotation':
                angle = data.get('angle', 0)
                command = RotationCommand(angle, current_image)
            elif operation_type == 'grayscale':
                command = GrayscaleCommand(current_image)
            elif operation_type == 'crop':
                box = data.get('crop_box')
                command = CropCommand(box, current_image)
            elif operation_type == 'resize':
                new_size = data.get('new_size')
                command = ResizeCommand(new_size, current_image)
            else:
                # Generic custom operation
                from models.command import CustomCommand
                modified_image = data.get('modified_image')
                if modified_image is None:
                    return
                # Use lambda to create the operation
                execute_func = lambda img: modified_image.copy()
                undo_func = lambda img: current_image.copy()
                command = CustomCommand(execute_func, undo_func, description)
            
            # Execute the command
            result = self.image_state.execute_command(command)
            
            if result:
                self.event_bus.publish("image_modified", {'image': result})
                self.event_bus.publish("undo_available", {'available': self.image_state.can_undo()})
                self.event_bus.publish("redo_available", {'available': self.image_state.can_redo()})
        except Exception as e:
            messagebox.showerror("Error", f"Unable to apply operation: {e}")
            self.event_bus.publish("redo_available", {'available': self.image_state.can_redo()})
        except Exception as e:
            messagebox.showerror("Error", f"Unable to apply operation: {e}")