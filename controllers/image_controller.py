"""Contrôleur principal pour les opérations sur l'image."""
from controllers.event_bus import EventBus
from models.image_state import ImageStateManager
from utils.image_operations import *
from customtkinter import filedialog
from tkinter import messagebox

class ImageController:
    """Gère la logique métier de l'application."""
    
    def __init__(self, event_bus: EventBus, image_state: ImageStateManager):
        self.event_bus = event_bus
        self.image_state = image_state
        
        # Abonnement aux événements
        self._subscribe_to_events()
    
    def _subscribe_to_events(self):
        """S'abonne aux événements du bus."""
        self.event_bus.subscribe("import_requested", self._handle_import)
        self.event_bus.subscribe("save_requested", self._handle_save)
        self.event_bus.subscribe("undo_requested", self._handle_undo)
        self.event_bus.subscribe("redo_requested", self._handle_redo)
        self.event_bus.subscribe("zoom_requested", self._handle_zoom)
        self.event_bus.subscribe("image_operation_applied", self._handle_operation)
    
    def _handle_import(self, data=None):
        """Gère l'import d'une image."""
        filetypes = [
            ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("Tous les fichiers", "*.*")
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
            self.event_bus.publish("image_loaded", image)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger l'image : {e}")
    
    def _handle_save(self, data=None):
        """Gère la sauvegarde de l'image."""
        current_image = self.image_state.get_current_image()
        
        if current_image is None:
            messagebox.showwarning("Attention", "Aucune image à sauvegarder")
            return
        
        filetypes = [
            ("PNG", "*.png"),
            ("JPEG", "*.jpg *.jpeg"),
            ("Tous les fichiers", "*.*")
        ]
        
        filepath = filedialog.asksaveasfilename(
            title="Enregistrer l'image",
            defaultextension=".png",
            filetypes=filetypes
        )
        
        if not filepath:
            return
        
        try:
            current_image.save(filepath)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer : {e}")
    
    def _handle_undo(self, data=None):
        """Gère l'annulation."""
        image = self.image_state.undo()
        
        if image:
            self.event_bus.publish("image_modified", image)
            self.event_bus.publish("status_message", "Action annulée")
        else:
            messagebox.showinfo("Info", "Rien à annuler")
    
    def _handle_redo(self, data=None):
        """Gère le refaire."""
        image = self.image_state.redo()
        
        if image:
            self.event_bus.publish("image_modified", image)
            self.event_bus.publish("status_message", "Action refaite")
        else:
            messagebox.showinfo("Info", "Rien à refaire")
    
    def _handle_zoom(self, zoom_delta: float):
        """Gère le changement de zoom."""
        self.event_bus.publish("zoom_changed", zoom_delta)
    
    def _handle_operation(self, modified_image):
        """Applique une opération sur l'image."""
        try:
            # Sauvegarde l'image modifiée dans l'état
            self.image_state.apply_operation(lambda img: modified_image)
            
            # Notifie les vues
            self.event_bus.publish("image_modified", modified_image)
            self.event_bus.publish("status_message", "Modification appliquée")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'appliquer l'opération : {e}")