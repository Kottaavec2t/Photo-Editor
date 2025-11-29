"""Popup pour recadrer l'image."""
import customtkinter as ctk
from PIL import Image
from views.popups.base_popup import BasePopup
from utils.image_operations import crop
from utils.validators import validate_numeric_input

class CropPopup(BasePopup):
    """Popup de recadrage d'image."""
    
    def __init__(self, master, image: Image.Image, event_bus):
        self.event_bus = event_bus
        super().__init__(master, image, "Recadrer l'image")
    
    def _create_controls(self):
        """Crée les contrôles de recadrage."""
        # Instructions
        ctk.CTkLabel(
            self.controls_frame,
            text="Définissez la zone de recadrage :",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Entrées pour les coordonnées
        self._create_coordinate_input("Gauche (Left)", "0", "left")
        self._create_coordinate_input("Haut (Top)", "0", "top")
        self._create_coordinate_input(
            "Droite (Right)",
            str(self.original_image.width),
            "right"
        )
        self._create_coordinate_input(
            "Bas (Bottom)",
            str(self.original_image.height),
            "bottom"
        )
        
        # Bouton Aperçu
        ctk.CTkButton(
            self.controls_frame,
            text="Aperçu du recadrage",
            command=self._preview_crop
        ).pack(pady=10)
        
        # Bouton Reset
        ctk.CTkButton(
            self.controls_frame,
            text="Réinitialiser",
            fg_color="red",
            command=self._reset
        ).pack(pady=5)
    
    def _create_coordinate_input(self, label: str, default: str, attr_name: str):
        """Crée un champ de saisie pour une coordonnée."""
        frame = ctk.CTkFrame(self.controls_frame)
        frame.pack(pady=5, padx=5, fill=ctk.X)
        
        ctk.CTkLabel(frame, text=label).pack(side=ctk.LEFT, padx=5)
        
        entry = ctk.CTkEntry(frame, width=100)
        entry.insert(0, default)
        entry.pack(side=ctk.RIGHT, padx=5)
        
        # Stocke l'entrée comme attribut
        setattr(self, f"{attr_name}_entry", entry)
    
    def _preview_crop(self):
        """Prévisualise le recadrage."""
        try:
            # Récupère et valide les coordonnées
            left = int(validate_numeric_input(
                self.left_entry.get(),
                min_val=0,
                max_val=self.original_image.width
            ))
            top = int(validate_numeric_input(
                self.top_entry.get(),
                min_val=0,
                max_val=self.original_image.height
            ))
            right = int(validate_numeric_input(
                self.right_entry.get(),
                min_val=left,
                max_val=self.original_image.width
            ))
            bottom = int(validate_numeric_input(
                self.bottom_entry.get(),
                min_val=top,
                max_val=self.original_image.height
            ))
            
            # Validation logique
            if right <= left or bottom <= top:
                raise ValueError("Les dimensions du recadrage sont invalides")
            
            # Applique le recadrage
            box = (left, top, right, bottom)
            self.current_image = crop(self.original_image, box)
            self._update_preview()
            
        except ValueError as e:
            self._show_error(str(e))
    
    def _reset(self):
        """Réinitialise les coordonnées."""
        self.left_entry.delete(0, 'end')
        self.left_entry.insert(0, "0")
        
        self.top_entry.delete(0, 'end')
        self.top_entry.insert(0, "0")
        
        self.right_entry.delete(0, 'end')
        self.right_entry.insert(0, str(self.original_image.width))
        
        self.bottom_entry.delete(0, 'end')
        self.bottom_entry.insert(0, str(self.original_image.height))
        
        self.current_image = self.original_image.copy()
        self._update_preview()
    
    def _on_apply(self):
        """Applique le recadrage et ferme."""
        if self.current_image != self.original_image:
            self.event_bus.publish("image_operation_applied", self.current_image)
        self.destroy()
    
    def _show_error(self, message: str):
        """Affiche un message d'erreur."""
        error_popup = ctk.CTkToplevel(self)
        error_popup.title("Erreur")
        error_popup.geometry("300x100")
        
        ctk.CTkLabel(error_popup, text=message).pack(pady=10)
        ctk.CTkButton(
            error_popup,
            text="OK",
            command=error_popup.destroy
        ).pack(pady=10)