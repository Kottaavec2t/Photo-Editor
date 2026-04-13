from views.main_window import MainWindow
from controllers import (
    ImageController, 
    EventBus,
    NotificationsController,
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
    image_controller = ImageController(event_bus, image_state)
    notifications_controller = NotificationsController(event_bus)
    
    app = MainWindow(event_bus, settings, icons)
    app.mainloop()
    
if __name__ == "__main__":
    main()