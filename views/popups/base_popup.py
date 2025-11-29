"""Classe de base pour toutes les fenêtres popup."""
import customtkinter as ctk
from PIL import Image
from abc import ABC, abstractmethod

class BasePopup(ctk.CTkToplevel, ABC):
    """Classe de base pour les popups modales."""
    
    def __init__(
        self,
        master,
        image: Image.Image,
        title: str,
        width: int = 600,
        height: int = 600
    ):
        super().__init__(master)
        
        self.original_image = image.copy()
        self.current_image = image.copy()
        
        # Configuration de la fenêtre
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        
        # Création de l'interface
        self._create_layout()
        self._create_controls()
        self._create_preview()
        self._create_action_buttons()
    
    def _create_layout(self):
        """Crée la disposition de base."""
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=5, pady=5)
        
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=5, pady=5)
    
    @abstractmethod
    def _create_controls(self):
        """Crée les contrôles spécifiques (à implémenter)."""
        pass
    
    def _create_preview(self):
        """Crée la zone de prévisualisation."""
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="Aperçu"
        )
        self.preview_label.pack(fill=ctk.BOTH, expand=True)
        self._update_preview()
    
    def _create_action_buttons(self):
        """Crée les boutons Apply et Cancel."""
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side=ctk.BOTTOM, fill=ctk.X, padx=5, pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="Annuler",
            command=self.destroy
        ).pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Appliquer",
            command=self._on_apply
        ).pack(side=ctk.RIGHT, padx=5)
    
    def _update_preview(self):
        """Met à jour l'aperçu de l'image."""
        if self.current_image:
            # Redimensionner pour l'aperçu
            preview_size = (400, 400)
            display_image = self.current_image.copy()
            display_image.thumbnail(preview_size, Image.Resampling.LANCZOS)
            
            ctk_image = ctk.CTkImage(
                display_image,
                size=(display_image.width, display_image.height)
            )
            self.preview_label.configure(image=ctk_image, text="")
    
    @abstractmethod
    def _on_apply(self):
        """Action lors de l'application (à implémenter)."""
        pass
    
    def get_result(self) -> Image.Image:
        """Retourne l'image modifiée."""
        return self.current_images