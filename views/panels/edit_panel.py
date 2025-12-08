import customtkinter as ctk
from views.panels.base_panel import BasePanel
from utils.validators import validate_numeric_input, validate_type
from utils.number_operations import clamp, round_number

class EditPanel(BasePanel):
    ''' Panneau d'édition des photos. '''

    def __init__(self, master, event_bus):
        super().__init__(master, event_bus)
        self.event_bus = event_bus
        self._setup_ui()

    def _setup_ui(self):
        ''' Setup the UI components of the edit panel. '''
        self.label = ctk.CTkLabel(self, text="Edit Panel")
        self.label.pack(side=ctk.TOP, padx=5, pady=5)

        # --[[ BRIGHTNESS ]]--
        self.brightness_frame = ctk.CTkFrame(self)
        self.brightness_frame.pack(fill=ctk.X, padx=5, pady=5)

        self.brightness_title_label = ctk.CTkLabel(self.brightness_frame, text='Brightness')
        self.brightness_title_label.pack(side=ctk.LEFT, padx=10, pady=5)

        self.brightness_value_var = ctk.StringVar(value="1.0")
        self.brightness_value_entry = ctk.CTkEntry(
            self.brightness_frame,
            textvariable=self.brightness_value_var
        )
        self.brightness_value_entry.bind("<FocusOut>", lambda e: self._brightness_changed(self.brightness_value_var.get(), event=e))
        self.brightness_value_entry.bind("<Return>", lambda e: self._brightness_changed(self.brightness_value_var.get(), event=e))
        self.brightness_value_entry.pack(side=ctk.LEFT, padx=10, pady=10)

        self.brightness_slider = ctk.CTkSlider(self.brightness_frame, from_=0, to=2, number_of_steps=200)
        self.brightness_slider.configure(command=self._brightness_changed)
        self.brightness_slider.pack(side=ctk.LEFT, padx=10, pady=10)

        # --[[ ROTATION ]]--
        self.rotation_frame = ctk.CTkFrame(self)
        self.rotation_frame.pack(fill=ctk.X, padx=5, pady=5)

        self.rotation_title_label = ctk.CTkLabel(self.rotation_frame, text='Rotation')
        self.rotation_title_label.pack(side=ctk.LEFT, padx=10, pady=5)
        self.rotation_value_var = ctk.StringVar(value="1.0")
        self.rotation_value_entry = ctk.CTkEntry(
            self.rotation_frame,
            textvariable=self.rotation_value_var
        )
        self.rotation_value_entry.bind("<FocusOut>", lambda e: self._rotation_changed(self.rotation_value_var.get(), event=e))
        self.rotation_value_entry.bind("<Return>", lambda e: self._rotation_changed(self.rotation_value_var.get(), event=e))
        self.rotation_value_entry.pack(side=ctk.LEFT, padx=10, pady=10)

        self.rotation_slider = ctk.CTkSlider(self.rotation_frame, from_=-180, to=180, number_of_steps=360)
        self.rotation_slider.configure(command=self._rotation_changed)
        self.rotation_slider.pack(side=ctk.LEFT, padx=10, pady=10)


    def _brightness_changed(self, value=None, event=None):
        ''' Handle brightness change events.
            Called either by slider or by entry validate.
            Rounds, validates, clamps and syncs both indicators.
            Publishes "edit_brightness_changed" event with {"value": float}.
        '''
        # guard: called early during widget init — bail out safely
        if not hasattr(self, "brightness_value_entry") or not hasattr(self, "brightness_slider"):
            return

        MIN, MAX = 0.0, 2.0

        # get input
        if value is None or not validate_type(value, float):
            value = self.brightness_slider.get()
            value = round_number(value) # round to avoid float precision issues
            if not validate_type(value, float):
                value = self.brightness_value_var.get()
                if not validate_type(value, float):
                    value = 1.0

        # Determine source
        if event is None and isinstance(value, float):
            value = round_number(value)

        # validate with existing validator; on ValueError clamp to bounds
        try:
            value = validate_numeric_input(value, min_val=MIN, max_val=MAX)
        except ValueError:
            value = clamp(float(value), MIN, MAX)

        # Sync the two indicators
        self.brightness_value_var.set(str(value))
        self.brightness_slider.set(value)

        self.event_bus.publish("edit_brightness_changed", {"value": value})

    def _rotation_changed(self, value=None, event=None):
        ''' Handle rotation change events.
            Called either by slider or by entry validate.
            Rounds, validates, clamps and syncs both indicators.
            Publishes "edit_rotation_changed" event with {"value": float}.
        '''
        # guard: called early during widget init — bail out safely
        if not hasattr(self, "rotation_value_entry") or not hasattr(self, "rotation_slider"):
            return

        MIN, MAX = -180.0, 180.0

        # get input
        if value is None or not validate_type(value, float):
            value = self.rotation_slider.get()
            value = round_number(value) # round to avoid float precision issues
            if not validate_type(value, float):
                value = self.rotation_value_var.get()
                if not validate_type(value, float):
                    value = 0.0

        # Determine source
        if event is None and isinstance(value, float):
            value = round_number(value, 0)

        # validate with existing validator; on ValueError clamp to bounds
        try:
            value = validate_numeric_input(value, min_val=MIN, max_val=MAX)
        except ValueError:
            value = clamp(float(value), MIN, MAX)

        # Sync the two indicators
        self.rotation_value_var.set(str(value))
        self.rotation_slider.set(value)

        self.event_bus.publish("edit_rotation_changed", {"value": value})
    