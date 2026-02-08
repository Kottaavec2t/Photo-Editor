from tkinter import messagebox, filedialog
from controllers import EventBus
from models import ImageStateManager
from models.commands import (
    BrightnessCommand,
    RotateCommand,
    GrayscaleCommand,
)

class ImageController:
    '''
    Handle image operations and communicate with the event bus.

    :param event_bus: The global event_bus to communicate with others scripts.
    :type event_bus: EventBus
    :param image_state: The global image_state to modify the image.
    :type image_state: ImageStateManager
    '''
    def __init__(self, event_bus: EventBus, image_state: ImageStateManager) -> None:
        self._event_bus = event_bus
        self._image_state = image_state
        self._setup_subscriptions()

    def _setup_subscriptions(self) -> None:
        '''
        Subscribe to events.
        '''
        self._event_bus.subscribe("import_requested", self._handle_import)
        self._event_bus.subscribe("save_requested", self._handle_save)
        self._event_bus.subscribe("undo_requested", self._handle_undo)
        self._event_bus.subscribe("redo_requested", self._handle_redo)
        self._event_bus.subscribe("image_operation_applied", self._handle_operation)

    def _handle_import(self, data: dict = None) -> None:
        '''
        Handle image import.

        :param data: Datas from event_bus.
        :type data: dict, optional
        '''
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
            self._image_state.load_image(filepath)
            image = self._image_state.get_current_image()
            print(image)
            self._event_bus.publish("image_loaded", {'image': image})
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load image: {e}")

    def _handle_save(self, data: dict = None) -> None:
        '''
        Handle image saving.

        :param data: Datas from event_bus.
        :type data: dict, optional
        '''
        current_image = self._image_state.get_current_image()
        
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

    def _handle_undo(self, data: dict = None) -> None:
        '''
        Handle undo.

        :param data: Datas from event_bus.
        :type data: dict, optional
        '''
        image = self._image_state.undo()
        
        if image:
            self._event_bus.publish("image_modified", {'image': image})
            # Notify that redo is available
            self._event_bus.publish("redo_available", {'available': self._image_state.can_redo()})
            # Notify that undo availability changed
            self._event_bus.publish("undo_available", {'available': self._image_state.can_undo()})
        else:
            messagebox.showinfo("Info", "Nothing to undo")

    def _handle_redo(self, data: dict = None) -> None:
        '''
        Handle redo.

        :param data: Datas from event_bus.
        :type data: dict, optional
        '''
        image = self._image_state.redo()
        
        if image:
            self._event_bus.publish("image_modified", {'image': image})
            # Notify that undo is available
            self._event_bus.publish("undo_available", {'available': self._image_state.can_undo()})
            # Notify that redo availability changed
            self._event_bus.publish("redo_available", {'available': self._image_state.can_redo()})
        else:
            messagebox.showinfo("Info", "Nothing to redo")

    def _handle_operation(self, data: dict = None) -> None:
        '''
        Apply an operation on the image.

        :param data: Datas from event_bus.
        :type data: dict, optional
        '''
        if data is None: return
        
        # Determine the operation type if provided
        operation_type = data.get('operation_type', None)
        
        # Create appropriate command based on type
        match operation_type:
            case 'brightness':
                factor = data.get('value', 1.0)
                command = BrightnessCommand(factor)
            case 'rotation':
                angle = data.get('angle', 0)
                command = RotateCommand(angle)
            case 'grayscale':
                value = data.get('value', False)
                command = GrayscaleCommand(value)
            case():
                print(f'Wrong operation type: {operation_type}')
                return
        
        # Execute the command
        result = self._image_state.execute_command(command, data.get('save', False))

        # Publish events
        if result:
            self._event_bus.publish("image_modified", {'image': result})
        self._event_bus.publish("undo_available", {'available': self._image_state.can_undo()})
        self._event_bus.publish("redo_available", {'available': self._image_state.can_redo()})
