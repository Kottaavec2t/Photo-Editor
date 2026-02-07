"""Point d'entrée de l'application Photo Editor."""
from views.main_window import MainWindow
from controllers import (
    ImageController, 
    EventBus,
)
from models import (
    ImageStateManager, 
    IconManager, 
    SettingsManager,
)

def main():
    '''
    Start application
    '''
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