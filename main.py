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
    Start application.
    '''
    event_bus = EventBus()
    image_state = ImageStateManager()
    icons = IconManager()
    settings = SettingsManager()
    controller = ImageController(event_bus, image_state)
    
    app = MainWindow(event_bus, settings, icons)
    app.mainloop()

if __name__ == "__main__":
    main()