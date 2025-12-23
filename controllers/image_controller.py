"""Contrôleur principal pour les opérations sur l'image."""
from controllers.event_bus import EventBus
from models.image_state import ImageStateManager
from utils.image_operations import *
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
        else:
            messagebox.showinfo("Info", "Nothing to undo")
    
    def _handle_redo(self, data: dict = None):
        """Handle redo."""
        image = self.image_state.redo()
        
        if image:
            self.event_bus.publish("image_modified", {'image': image})
        else:
            messagebox.showinfo("Info", "Nothing to redo")
    
    def _handle_operation(self, data: dict = None):
        """Apply an operation on the image."""
        try:
            # Save the modified image in the state
            self.image_state.apply_operation(lambda img: data['modified_image'])
            
            # Notify the views
            self.event_bus.publish("image_modified", {'image': data['modified_image']})
        except Exception as e:
            messagebox.showerror("Error", f"Unable to apply operation: {e}")