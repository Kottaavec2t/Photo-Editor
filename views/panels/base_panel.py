import customtkinter as ctk

class BasePanel(ctk.CTkFrame):
    def __init__(self, master, event_bus):
        super().__init__(master)
        self.event_bus = event_bus