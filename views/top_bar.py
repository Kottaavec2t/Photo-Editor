"""Barre d'outils supérieure complète."""
import customtkinter as ctk
from controllers.event_bus import EventBus

class TopBar(ctk.CTkFrame):
    """Barre d'outils complète avec tous les widgets."""
    
    def __init__(self, master, event_bus: EventBus):
        super().__init__(master)
        self.event_bus = event_bus
        self.configure(height=40)
        
        # Création de tous les widgets
        self._create_menu_button()
        self._create_action_buttons()
        self._create_file_buttons()
        self._create_zoom_buttons()
        self._create_edit_buttons()
        self._create_search_bar()
        
        # Abonnements aux événements
        self._setup_subscriptions()
    
    def _create_menu_button(self):
        """Bouton menu avec 3 lignes horizontales."""
        self.menu_btn = ctk.CTkButton(
            self,
            text="☰",
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_menu_click
        )
        self.menu_btn.pack(side=ctk.LEFT, padx=5, pady=5)
    
    def _create_action_buttons(self):
        """Boutons Undo/Redo."""
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(side=ctk.LEFT, padx=5, pady=5)
        
        self.undo_btn = ctk.CTkButton(
            action_frame,
            text="↶",
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_undo_click,
            state="disabled"
        )
        self.undo_btn.grid(row=0, column=0, padx=2)
        
        self.redo_btn = ctk.CTkButton(
            action_frame,
            text="↷",
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
            text="📂",
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_import_click
        )
        self.import_btn.grid(row=0, column=0, padx=2)
        
        self.save_btn = ctk.CTkButton(
            file_frame,
            text="💾",
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
            text="🔍+",
            width=30,
            height=30,
            fg_color="transparent",
            command=lambda: self._on_zoom_click(0.1),
            state="disabled"
        )
        self.zoom_out_btn.grid(row=0, column=0, padx=2)
        
        self.zoom_in_btn = ctk.CTkButton(
            zoom_frame,
            text="🔍-",
            width=30,
            height=30,
            fg_color="transparent",
            command=lambda: self._on_zoom_click(-0.1),
            state="disabled"
        )
        self.zoom_in_btn.grid(row=0, column=1, padx=2)
    
    def _create_edit_buttons(self):
        """Boutons Edit/Crop."""
        edit_frame = ctk.CTkFrame(self, fg_color="transparent")
        edit_frame.pack(side=ctk.LEFT, padx=5, pady=5)
        
        self.edit_btn = ctk.CTkButton(
            edit_frame,
            text="✏️",
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_edit_click,
            state="disabled"
        )
        self.edit_btn.grid(row=0, column=0, padx=2)
        
        self.crop_btn = ctk.CTkButton(
            edit_frame,
            text="✂️",
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_crop_click,
            state="disabled"
        )
        self.crop_btn.grid(row=0, column=1, padx=2)
    
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
            text="✕",
            width=30,
            height=30,
            fg_color="transparent",
            command=self._on_clear_search
        )
        self.clear_btn.grid(row=0, column=1, padx=2)
        
        # Bouton Search
        self.search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
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
    
    def _on_menu_click(self):
        """Ouvre le menu principal."""
        self.event_bus.publish("menu_requested")
    
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
        self.event_bus.publish("zoom_changed", delta)
    
    def _on_edit_click(self):
        """Ouvre la popup d'édition."""
        self.event_bus.publish("edit_requested")
    
    def _on_crop_click(self):
        """Ouvre la popup de crop."""
        self.event_bus.publish("crop_requested")
    
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
            self.event_bus.publish("search_requested", query)
    
    def _on_clear_search(self):
        """Efface la barre de recherche."""
        self.search_entry.delete(0, 'end')
    
    def _execute_command(self, command: str):
        """Exécute une commande slash."""
        parts = command.split(' ')
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        commands = {
            '/help': self._cmd_help,
            '/state': self._cmd_state,
            '/theme': self._cmd_theme,
            '/appearance': self._cmd_appearance,
            '/restart': self._cmd_restart,
            '/about': self._cmd_about,
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
    
    def _cmd_help(self, args):
        """Affiche l'aide des commandes."""
        help_text = """
Commandes disponibles :
/help - Affiche cette aide
/state [normal|zoomed] - Change l'état de la fenêtre
/theme [blue|green|dark-blue] - Change le thème
/appearance [Dark|Light|System] - Change l'apparence
/restart - Redémarre l'application
/about - À propos de l'application
        """.strip()
        
        self.event_bus.publish("show_message", {
            "type": "info",
            "text": help_text
        })
    
    def _cmd_state(self, args):
        """Change l'état de la fenêtre."""
        if not args:
            self.event_bus.publish("show_message", {
                "type": "error",
                "text": "Usage: /state [normal|zoomed]"
            })
            return
        
        state = args[0].lower()
        if state in ['normal', 'zoomed']:
            self.event_bus.publish("window_state_change", state)
        else:
            self.event_bus.publish("show_message", {
                "type": "error",
                "text": "État invalide. Utilisez 'normal' ou 'zoomed'."
            })
    
    def _cmd_theme(self, args):
        """Change le thème de couleur."""
        if not args:
            self.event_bus.publish("show_message", {
                "type": "error",
                "text": "Usage: /theme [blue|green|dark-blue]"
            })
            return
        
        theme = args[0].lower()
        if theme in ['blue', 'green', 'dark-blue']:
            self.event_bus.publish("theme_change", theme)
            self.event_bus.publish("show_message", {
                "type": "success",
                "text": f"Thème changé en {theme}. Redémarrez pour voir les changements."
            })
        else:
            self.event_bus.publish("show_message", {
                "type": "error",
                "text": "Thème invalide. Choisissez: blue, green, dark-blue"
            })
    
    def _cmd_appearance(self, args):
        """Change le mode d'apparence."""
        if not args:
            self.event_bus.publish("show_message", {
                "type": "error",
                "text": "Usage: /appearance [Dark|Light|System]"
            })
            return
        
        appearance = args[0].capitalize()
        if appearance in ['Dark', 'Light', 'System']:
            self.event_bus.publish("appearance_change", appearance)
            self.event_bus.publish("show_message", {
                "type": "success",
                "text": f"Apparence changée en {appearance}"
            })
        else:
            self.event_bus.publish("show_message", {
                "type": "error",
                "text": "Apparence invalide. Choisissez: Dark, Light, System"
            })
    
    def _cmd_restart(self, args):
        """Redémarre l'application."""
        self.event_bus.publish("restart_requested")
    
    def _cmd_about(self, args):
        """Affiche les infos de l'application."""
        about_text = """
Photo Editor v1.0
Architecture refactorisée avec Event Bus
Développé avec CustomTkinter et PIL
        """.strip()
        
        self.event_bus.publish("show_message", {
            "type": "info",
            "text": about_text
        })
    
    # --[[ Mise à jour de l'interface ]]--
    
    def _on_image_loaded(self, data: dict = None):
        """Active les boutons quand une image est chargée."""
        self.save_btn.configure(state="normal")
        self.zoom_out_btn.configure(state="normal")
        self.zoom_in_btn.configure(state="normal")
        self.edit_btn.configure(state="normal")
        self.crop_btn.configure(state="normal")
    
    def _on_image_modified(self, data: dict = None):
        """Réagit à la modification d'image."""
        pass
    
    def _update_undo_button(self, available: bool):
        """Active/désactive le bouton Undo."""
        self.undo_btn.configure(state="normal" if available else "disabled")
        # Maybe change color to indicate availability

    def _update_redo_button(self, available: bool):
        """Active/désactive le bouton Redo."""
        self.redo_btn.configure(state="normal" if available else "disabled")
        # Maybe change color to indicate availability