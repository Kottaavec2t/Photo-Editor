"""Barre d'outils supérieure complète."""
import customtkinter as ctk
from controllers.event_bus import EventBus
from models.icons import IconManager
from models.settings import SettingsManager

class TopBar(ctk.CTkFrame):
    """Barre d'outils complète avec tous les widgets."""
    
    def __init__(self, master, event_bus: EventBus, settings: SettingsManager, icons: IconManager):
        super().__init__(master)
        self.event_bus = event_bus
        self.settings = settings
        self.icons = icons
        self.configure(height=40)
        
        # Création de tous les widgets
        self._create_action_buttons()
        self._create_file_buttons()
        self._create_zoom_buttons()
        self._create_search_bar()
        
        # Abonnements aux événements
        self._setup_subscriptions()
    
    def _create_action_buttons(self):
        '''
        Boutons Undo/Redo
        '''
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(side=ctk.LEFT, padx=5, pady=5)
        
        self.undo_btn = ctk.CTkButton(
            action_frame,
            text='',
            image=self.icons.get('undo'),
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_undo_click,
            state="disabled"
        )
        self.undo_btn.grid(row=0, column=0, padx=2)
        
        self.redo_btn = ctk.CTkButton(
            action_frame,
            text='',
            image=self.icons.get('redo'),
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_redo_click,
            state="disabled"
        )
        self.redo_btn.grid(row=0, column=1, padx=2)
    
    def _create_file_buttons(self):
        """Boutons Import/Save."""
        file_frame = ctk.CTkFrame(self, fg_color="transparent")
        file_frame.pack(side=ctk.LEFT, padx=5, pady=5)
        
        self.import_btn = ctk.CTkButton(
            file_frame,
            text='',
            image=self.icons.get('open-folder'),
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_import_click
        )
        self.import_btn.grid(row=0, column=0, padx=2)
        
        self.save_btn = ctk.CTkButton(
            file_frame,
            text='',
            image=self.icons.get('save'),
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_save_click,
            state="disabled"
        )
        self.save_btn.grid(row=0, column=1, padx=2)
    
    def _create_zoom_buttons(self):
        """Boutons Zoom In/Out."""
        zoom_frame = ctk.CTkFrame(self, fg_color="transparent")
        zoom_frame.pack(side=ctk.LEFT, padx=5, pady=5)
        
        self.zoom_out_btn = ctk.CTkButton(
            zoom_frame,
            text='',
            image=self.icons.get('zoom-out'),
            width=30,
            height=30,
            fg_color="transparent",
            command=lambda: self._on_zoom_click(0.1),
            state="disabled"
        )
        self.zoom_out_btn.grid(row=0, column=0, padx=2)
        
        self.zoom_in_btn = ctk.CTkButton(
            zoom_frame,
            text='',
            image=self.icons.get('zoom-in'),
            width=30,
            height=30,
            fg_color="transparent",
            command=lambda: self._on_zoom_click(-0.1),
            state="disabled"
        )
        self.zoom_in_btn.grid(row=0, column=1, padx=2)
    
    def _create_search_bar(self):
        """Barre de recherche avec boutons."""
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(padx=5, pady=5)
        
        # Entry de recherche
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Rechercher... (commandes: /help)",
            width=200,
            height=30,
            border_width=1,
            corner_radius=10,
            fg_color="transparent"
        )
        self.search_entry.grid(row=0, column=0, padx=5)
        self.search_entry.bind("<Return>", lambda e: self._on_search())
        
        # Bouton Clear
        self.clear_btn = ctk.CTkButton(
            search_frame,
            text='',
            image=self.icons.get('cross'),
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_clear_search
        )
        self.clear_btn.grid(row=0, column=1, padx=2)
        
        # Bouton Search
        self.search_btn = ctk.CTkButton(
            search_frame,
            text='',
            image=self.icons.get('search'),
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_search
        )
        self.search_btn.grid(row=0, column=2, padx=2)
    
    def _setup_subscriptions(self):
        """S'abonne aux événements pour mettre à jour l'UI."""
        self.event_bus.subscribe("image_loaded", self._on_image_loaded)
        self.event_bus.subscribe("image_modified", self._on_image_modified)
        self.event_bus.subscribe("undo_available", self._update_undo_button)
        self.event_bus.subscribe("redo_available", self._update_redo_button)
    
    # --[[ Gestionnaire de clics ]]--
    
    def _on_undo_click(self):
        """Demande l'annulation."""
        self.event_bus.publish("undo_requested")
    
    def _on_redo_click(self):
        """Demande de refaire."""
        self.event_bus.publish("redo_requested")
    
    def _on_import_click(self):
        """Demande l'import d'une image."""
        self.event_bus.publish("import_requested")
    
    def _on_save_click(self):
        """Demande la sauvegarde."""
        self.event_bus.publish("save_requested")
    
    def _on_zoom_click(self, delta: float):
        """Demande un changement de zoom."""
        self.event_bus.publish("zoom_changed", {'zoom_delta': delta})
    
    def _on_search(self):
        """Exécute la recherche ou commande."""
        query = self.search_entry.get().strip()
        
        if not query:
            return
        
        # Détection de commandes (commence par /)
        if query.startswith('/'):
            self._execute_command(query)
        else:
            # Recherche normale
            self.event_bus.publish("search_requested", {'query': query})
    
    def _on_clear_search(self):
        """Efface la barre de recherche."""
        self.search_entry.delete(0, 'end')
    
    def _execute_command(self, command: str):
        """Exécute une commande slash."""
        parts = command.split(' ')
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        commands = {
            '/restart': self._cmd_restart,
        }
        
        if cmd in commands:
            commands[cmd](args)
        else:
            self.event_bus.publish("show_message", {
                "type": "error",
                "text": f"Commande inconnue : {cmd}. Tapez /help pour la liste."
            })
        
        # Efface la commande après exécution
        self.search_entry.delete(0, 'end')
    
    # --[[ Commandes slash ]]--
    
    def _cmd_restart(self, args):
        """Redémarre l'application."""
        self.event_bus.publish("restart_requested")
    
    # --[[ Mise à jour de l'interface ]]--
    
    def _on_image_loaded(self, data: dict = None):
        """Active les boutons quand une image est chargée."""
        self.save_btn.configure(state="normal")
        self.zoom_out_btn.configure(state="normal")
        self.zoom_in_btn.configure(state="normal")
    
    def _on_image_modified(self, data: dict = None):
        """Réagit à la modification d'image."""
        pass
    
    def _update_undo_button(self, data: dict = None):
        """Active/désactive le bouton Undo."""
        available = data.get("available", False) if data else False
        self.undo_btn.configure(state="normal" if available else "disabled")
        # Maybe change color to indicate availability

    def _update_redo_button(self, data: dict = None):
        """Active/désactive le bouton Redo."""
        available = data.get("available", False) if data else False
        self.redo_btn.configure(state="normal" if available else "disabled")
        # Maybe change color to indicate availability