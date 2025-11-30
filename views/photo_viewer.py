"""Widget d'affichage d'image avec zoom."""
import customtkinter as ctk
from PIL import Image, ImageTk
from controllers.event_bus import EventBus

class PhotoViewer(ctk.CTkFrame):
    """Affiche l'image avec zoom et défilement."""
    
    def __init__(self, master, event_bus: EventBus):
        super().__init__(master, fg_color="transparent")
        self.event_bus = event_bus
        self.zoom = 1.0
        self.current_image = None
        
        self._create_widgets()
        self._setup_bindings() # ! After the widgets are created !
        self._setup_subscriptions()
    
    def _create_widgets(self):
        """Crée le canvas et les scrollbars."""
        # Scrollbars
        self.yscroll = ctk.CTkScrollbar(self, orientation=ctk.VERTICAL)
        self.yscroll.pack(side=ctk.RIGHT, fill=ctk.Y)
        
        self.xscroll = ctk.CTkScrollbar(self, orientation=ctk.HORIZONTAL)
        self.xscroll.pack(side=ctk.BOTTOM, fill=ctk.X)
        
        # Canvas
        self.canvas = ctk.CTkCanvas(
            self,
            yscrollcommand=self.yscroll.set,
            xscrollcommand=self.xscroll.set,
            bg=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]
        )
        self.canvas.pack(fill=ctk.BOTH, expand=True)
        
        self.yscroll.configure(command=self.canvas.yview)
        self.xscroll.configure(command=self.canvas.xview)
        
        # Label pour l'image
        self.image_label = ctk.CTkLabel(self.canvas, text="Aucune image")
        self.canvas_window = self.canvas.create_window(
            0, 0,
            anchor=ctk.NW,
            window=self.image_label
        )

    def _setup_bindings(self):
        """Configure les bindings d'événements."""
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Control-MouseWheel>", self._on_ctrl_mousewheel)
    
    def _setup_subscriptions(self):
        """S'abonne aux événements du bus."""
        self.event_bus.subscribe("image_loaded", self._on_image_update)
        self.event_bus.subscribe("image_modified", self._on_image_update)
        self.event_bus.subscribe("zoom_changed", self._on_zoom_changed)
    
    def _on_image_update(self, image: Image.Image):
        """Met à jour l'affichage avec la nouvelle image."""
        print('test')
        self.current_image = image
        self._update_display()
    
    def _update_display(self):
        """Redessine l'image avec le zoom actuel."""
        if self.current_image is None:
            return
        
        # Calcul de la taille avec zoom
        width = int(self.current_image.width * self.zoom)
        height = int(self.current_image.height * self.zoom)
        
        # Création de l'image CTk
        ctk_image = ctk.CTkImage(
            self.current_image,
            size=(width, height)
        )
        print('Updating display with zoom:', self.zoom)
        self.image_label.configure(image=ctk_image, text="")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_mousewheel(self, event):
        """Gère le défilement."""
        if self._is_scrollbar_active('y'):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _on_alt_mousewheel(self, event):
        """Gère le défilement horizontal avec Alt+molette."""
        if self._is_scrollbar_active('x'):
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _on_ctrl_mousewheel(self, event):
        """Gère le zoom avec Ctrl+molette."""
        if event.delta > 0:
            self.event_bus.publish("zoom_requested", 0.1)
        else:
            self.event_bus.publish("zoom_requested", -0.1)
    
    def _on_zoom_changed(self, zoom_delta: float):
        """Applique le changement de zoom."""
        new_zoom = self.zoom + zoom_delta
        if 0.1 <= new_zoom <= 10:
            self.zoom = new_zoom
            self._update_display()