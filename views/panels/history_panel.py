import customtkinter as ctk
from views.panels import BasePanel
from controllers import EventBus

class HistoryPanel(BasePanel):
    '''
    Panel for viewing photo edit history.

    :param event_bus: The global event_bus to communicate with others scripts.
    :type event_bus: EventBus
    '''
    def __init__(self, master, event_bus: EventBus) -> None:
        super().__init__(master, event_bus)
        self._event_bus = event_bus
        self._undo_stack = []
        self._redo_stack = []
        self._setup_subscriptions()
        self._setup_ui()

    def _setup_subscriptions(self) -> None:
        '''
        Subscribe to events.
        '''
        self._event_bus.subscribe("history_updated", self._update_history)

    def _setup_ui(self) -> None:
        '''
        Setup the UI components of the history panel.
        '''
        self.label = ctk.CTkLabel(self, text="History Panel")
        self.label.pack(side=ctk.TOP, padx=5, pady=5)

        self.top_buttons_frame = ctk.CTkFrame(self)
        self.top_buttons_frame.pack(fill=ctk.X, padx=5, pady=5)

        self.undo_button = ctk.CTkButton(self.top_buttons_frame, text="Undo Commands")
        self.undo_button.configure(command=self._undo_button_command)
        self.undo_button.pack(expand=True, side=ctk.LEFT, fill=ctk.X, padx=5, pady=10)
        
        self.redo_button = ctk.CTkButton(self.top_buttons_frame, text="Redo Commands")
        self.redo_button.configure(command=self._redo_button_command)
        self.redo_button.pack(expand=True, side=ctk.LEFT, fill=ctk.X, padx=5, pady=10)

        self.undo_frame = ctk.CTkScrollableFrame(self)
        self.undo_frame.columnconfigure(0, weight=1)
        self.undo_frame.pack(fill=ctk.BOTH, padx=5, pady=5)

        self.redo_frame = ctk.CTkScrollableFrame(self)
        self.redo_frame.columnconfigure(0, weight=1)

        self._update_command_grid_ui()

    def _update_command_grid_ui(self) -> None:
        '''
        Update the two commands list.
        '''
        self._clear_frame(self.undo_frame)
        self._clear_frame(self.redo_frame)
        if self._undo_stack == [] and self._redo_stack == []: return
        for i, current_command in enumerate(reversed(self._undo_stack)):
            current_label = ctk.CTkLabel(self.undo_frame, text=current_command.get_description())
            current_label.grid(column=0, row=i)
        for i, current_command in enumerate(reversed(self._redo_stack)):
            current_label = ctk.CTkLabel(self.redo_frame, text=current_command.get_description())
            current_label.grid(column=0, row=i)

    def _update_history(self, data: dict = None) -> None:
        '''
        Update the stacks.
        Update the two commands list.

        :param data: Datas from event_bus.
        :type data: dict, optional
        '''
        self._undo_stack = data.get('undo_stack', self._undo_stack)
        self._redo_stack = data.get('redo_stack', self._redo_stack)
        self._update_command_grid_ui()

    def _undo_button_command(self) -> None:
        '''
        Command fired when undo button clicked.
        Change the packed frame.
        '''
        self.redo_frame.pack_forget()
        self.undo_frame.pack(fill=ctk.BOTH, padx=5, pady=5)

    def _redo_button_command(self) -> None:
        '''
        Command fired when redo button clicked.
        Change the packed frame.
        '''
        self.redo_frame.pack(fill=ctk.BOTH, padx=5, pady=5)
        self.undo_frame.pack_forget()

    def _clear_frame(self, frame: ctk.CTkFrame) -> None:
        '''
        Destroy all the widgets in the frame.

        :param frame: The frame to clear.
        :type frame: ctk.CtkFrame
        '''
        for w in frame.winfo_children():
            w.destroy()