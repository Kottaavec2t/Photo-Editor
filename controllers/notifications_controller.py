from tkinter import messagebox
from controllers import EventBus

class NotificationsController:
    '''
    '''
    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._setup_subscriptions()

    def _setup_subscriptions(self) -> None:
        '''
        Subscribe to events.
        '''
        self._event_bus.subscribe("info_notification", self._info_notification)
        self._event_bus.subscribe("error_notification", self._error_notification)

    def _info_notification(self, data: dict = None) -> None:
        title = data.get("title", "Info")
        corpse = data.get("corpse", "")

        messagebox.showinfo(title, corpse, icon=messagebox.INFO)

    def _error_notification(self, data: dict = None) -> None:
        title = data.get("title", "Error")
        corpse = data.get("corpse", "")

        messagebox.showerror(title, corpse, icon=messagebox.ERROR)
