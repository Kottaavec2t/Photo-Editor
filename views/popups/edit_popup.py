"""Popup pour éditer l'image."""
import customtkinter as ctk
from PIL import Image
from views.popups.base_popup import BasePopup
from utils.image_operations import (
    to_grayscale,
    adjust_brightness,
    rotate,
    resize
)
from utils.validators import validate_numeric_input

class EditPopup(BasePopup):
    """Popup d'édition d'image."""
    
    def __init__(self, master, image: Image.Image, event_bus):
        self.event_bus = event_bus
        super().__init__(master, image, "Éditer l'image")
    
    def _create_controls(self):
        """Crée les contrôles d'édition."""
        # Noir & Blanc
        bw_frame = self._create_section("Noir & Blanc")
        ctk.CTkButton(
            bw_frame,
            text="Appliquer N&B",
            command=self._apply_grayscale
        ).pack(pady=5)
        
        # Luminosité
        brightness_frame = self._create_section("Luminosité")
        self.brightness_entry = ctk.CTkEntry(
            brightness_frame,
            placeholder_text="Facteur (0.5 - 2.0)"
        )
        self.brightness_entry.pack(pady=5)
        ctk.CTkButton(
            brightness_frame,
            text="Appliquer",
            command=self._apply_brightness
        ).pack(pady=5)
        
        # Rotation
        rotation_frame = self._create_section("Rotation")
        self.rotation_entry = ctk.CTkEntry(
            rotation_frame,
            placeholder_text="Angle (degrés)"
        )
        self.rotation_entry.pack(pady=5)
        ctk.CTkButton(
            rotation_frame,
            text="Pivoter",
            command=self._apply_rotation
        ).pack(pady=5)
        
        # Reset
        ctk.CTkButton(
            self.controls_frame,
            text="Réinitialiser",
            fg_color="red",
            command=self._reset
        ).pack(pady=10)
    
    def _create_section(self, title: str) -> ctk.CTkFrame:
        """Crée une section avec titre."""
        frame = ctk.CTkFrame(self.controls_frame)
        frame.pack(pady=10, padx=5, fill=ctk.X)
        
        ctk.CTkLabel(frame, text=title, font=("Arial", 12, "bold")).pack(pady=5)
        return frame
    
    def _apply_grayscale(self):
        """Applique le filtre noir et blanc."""
        self.current_image = to_grayscale(self.current_image)
        self._update_preview()
    
    def _apply_brightness(self):
        """Applique le changement de luminosité."""
        try:
            factor = validate_numeric_input(
                self.brightness_entry.get(),
                min_val=0.1,
                max_val=3.0
            )
            self.current_image = adjust_brightness(self.current_image, factor)
            self._update_preview()
        except ValueError as e:
            self._show_error(str(e))
    
    def _apply_rotation(self):
        """Applique la rotation."""
        try:
            angle = validate_numeric_input(self.rotation_entry.get())
            self.current_image = rotate(self.original_image, angle)
            self._update_preview()
        except ValueError as e:
            self._show_error(str(e))
    
    def _reset(self):
        """Réinitialise à l'image originale."""
        self.current_image = self.original_image.copy()
        self._update_preview()
    
    def _on_apply(self):
        """Applique les modifications et ferme."""
        self.event_bus.publish("image_operation_applied", self.current_image)
        self.destroy()
    
    def _show_error(self, message: str):
        """Affiche un message d'erreur."""
        # Création d'une petite popup d'erreur
        error_popup = ctk.CTkToplevel(self)
        error_popup.title("Erreur")
        error_popup.geometry("300x100")
        
        ctk.CTkLabel(error_popup, text=message).pack(pady=10)
        ctk.CTkButton(
            error_popup,
            text="OK",
            command=error_popup.destroy
        ).pack(pady=10)