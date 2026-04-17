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
        self._event_bus.subscribe("warning_notification", self._warning_notification)
        self._event_bus.subscribe("yesno_notification", self._yesno_question)
        self._event_bus.subscribe("okcancel_notification", self._okcancel_question)
        self._event_bus.subscribe("retrycancel_notification", self._retrycancel_question)
        self._event_bus.subscribe("yesnocancel_notification", self._yesnocancel_question)

    def _info_notification(self, data: dict = None) -> None:
        title = data.get("title", "Info")
        corpse = data.get("corpse", "")

        messagebox.showinfo(title, corpse, icon=messagebox.INFO)

    def _error_notification(self, data: dict = None) -> None:
        title = data.get("title", "Error")
        corpse = data.get("corpse", "")

        messagebox.showerror(title, corpse, icon=messagebox.ERROR)

    def _warning_notification(self, data: dict = None) -> None:
        title = data.get("title", "Warning")
        corpse = data.get("corpse", "")

        messagebox.showwarning(title, corpse, icon=messagebox.WARNING)

    def _yesno_question(self, data: dict = None) -> bool | None:
        title = data.get("title", "Confirmation")
        corpse = data.get("corpse", "")
        icon = data.get("icon", messagebox.YESNO)

        return messagebox.askquestion(title, corpse, icon=icon, type=messagebox.YESNO)
    
    def _okcancel_question(self, data: dict = None) -> bool | None:
        title = data.get("title", "Confirmation")
        corpse = data.get("corpse", "")
        icon = data.get("icon", messagebox.OKCANCEL)

        return messagebox.askquestion(title, corpse, icon=icon, type=messagebox.OKCANCEL)
    
    def _retrycancel_question(self, data: dict = None) -> bool | None:
        title = data.get("title", "Confirmation")
        corpse = data.get("corpse", "")
        icon = data.get("icon", messagebox.RETRYCANCEL)

        return messagebox.askquestion(title, corpse, icon=icon, type=messagebox.RETRYCANCEL)
    
    def _yesnocancel_question(self, data: dict = None) -> bool | None:
        title = data.get("title", "Confirmation")
        corpse = data.get("corpse", "")
        icon = data.get("icon", messagebox.YESNOCANCEL)

        return messagebox.askquestion(title, corpse, icon=icon, type=messagebox.YESNOCANCEL)
