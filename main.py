"""Point d'entrée de l'application Photo Editor."""
from views.main_window import MainWindow
from controllers.image_controller import ImageController
from controllers.event_bus import EventBus
from models.image_state import ImageStateManager
from models.icons import IconManager
from models.settings import SettingsManager

def main():
    """Lance l'application."""
    # Initialisation des composants centraux
    event_bus = EventBus()
    image_state = ImageStateManager()
    icons = IconManager()
    settings = SettingsManager()
    controller = ImageController(event_bus, image_state)
    
    # Création et lancement de la fenêtre principale
    app = MainWindow(event_bus, settings, icons)
    app.mainloop()

if __name__ == "__main__":
    main()