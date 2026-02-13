import customtkinter as ctk
from controllers import EventBus
from models import SettingsManager

class PhotoViewer(ctk.CTkFrame):
    '''
    Display image with zoom and movements UBLR.

    :param event_bus: The global event_bus to communicate with others scripts.
    :type event_bus: EventBus
    :param settings: The global settings manager to access settings from nowhere.
    :type settings: SettingsManager
    '''
    def __init__(self, master, event_bus: EventBus, settings: SettingsManager) -> None:
        super().__init__(master, fg_color="transparent")
        self._event_bus = event_bus
        self._settings = settings
        self._zoom = 1.0
        self._current_image = None
        
        self._create_widgets()
        self._setup_bindings() # ! After the widgets are created !
        self._setup_subscriptions()

    def _create_widgets(self) -> None:
        '''
        Create widgets.
        Canvas + Scrollbars.
        '''
        self.yscroll = ctk.CTkScrollbar(self, orientation=ctk.VERTICAL)
        self.yscroll.pack(side=ctk.RIGHT, fill=ctk.Y)
        
        self.xscroll = ctk.CTkScrollbar(self, orientation=ctk.HORIZONTAL)
        self.xscroll.pack(side=ctk.BOTTOM, fill=ctk.X)
        
        # Canvas
        self.canvas = ctk.CTkCanvas(
            self,
            yscrollcommand=self.yscroll.set,
            xscrollcommand=self.xscroll.set,
            bg=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1] if self._settings.get("appearance") == 'Dark' else None,
            highlightthickness=0, 
            relief='ridge'
        )
        self.canvas.pack(fill=ctk.BOTH, expand=True)
        
        self.yscroll.configure(command=self.canvas.yview)
        self.xscroll.configure(command=self.canvas.xview)
        
        # Label for the image
        self.image_label = ctk.CTkLabel(self.canvas, text="")
        self.canvas_window = self.canvas.create_window(
            0, 0,
            window=self.image_label
        )

    def _setup_bindings(self) -> None:
        '''
        Setup event bindings.
        '''
        self.image_label.bind("<MouseWheel>", self._on_mousewheel)
        self.image_label.bind("<Alt-MouseWheel>", self._on_alt_mousewheel)
        self.image_label.bind("<Control-MouseWheel>", self._on_ctrl_mousewheel)

    def _setup_subscriptions(self) -> None:
        '''
        Subscribe to events.
        '''
        self._event_bus.subscribe("image_loaded", self._on_image_update)
        self._event_bus.subscribe("image_modified", self._on_image_update)
        self._event_bus.subscribe("zoom_changed", self._on_zoom_changed)

    def _on_image_update(self, data: dict = None) -> None:
        '''
        Update display with new image.
        
        :param data: Datas from event_bus.
        :type data: dict, optional
        '''
        self._current_image = data['image']
        self._update_display()

    def _update_display(self) -> None:
        '''
        Resize image with new zoom.
        '''
        if self._current_image is None: return
        
        width = int(self._current_image.width * self._zoom)
        height = int(self._current_image.height * self._zoom)
        
        ctk_image = ctk.CTkImage(
            self._current_image,
            size=(width, height)
        )
        self.image_label.configure(image=ctk_image, text="")

        # Center image
        self.canvas.update_idletasks()
        self.canvas.coords(self.canvas_window, self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event) -> None:
        '''
        Manage scrolling with scrollwheel.
        
        :param event: Event gived by CtkWidget
        :type event: any, optional
        '''
        if self._is_scrollbar_active('y'):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_alt_mousewheel(self, event) -> None:
        '''
        Manage scrolling with alt+scrollwheel.

        :param event: Event gived by CtkWidget
        :type event: any, optional
        '''
        if self._is_scrollbar_active('x'):
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_ctrl_mousewheel(self, event) -> None:
        '''
        Manage zooming with ctrl+scrollwheel.

        :param event: Event gived by CtkWidget
        :type event: any, optional
        '''
        if event.delta > 0:
            self._event_bus.publish("zoom_changed", {'zoom_delta': 0.1})
        else:
            self._event_bus.publish("zoom_changed", {'zoom_delta': -0.1})

    def _on_zoom_changed(self, data: dict = None) -> None:
        '''
        Manage zoom changed.
        
        :param data: Datas from event_bus.
        :type data: dict, optional
        '''
        new_zoom = self._zoom + data['zoom_delta']
        if 0.1 <= new_zoom <= 10:
            self._zoom = new_zoom
            self._update_display()

    def _is_scrollbar_active(self, axe: str ="x") -> bool:
        '''
        Check if scrollbars need to be activates (image is too zoomed for the screen).

        :param axe: The axe (x or y) to check scrollbar for.
        :type axe: str, optional
        '''
        self.canvas.update_idletasks()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        scroll_region = self.canvas.cget("scrollregion")
        if scroll_region:
            coords = scroll_region.split()
            if len(coords) == 4:
                content_width = float(coords[2]) - float(coords[0])
                content_height = float(coords[3]) - float(coords[1])
                
                if axe == 'y': return content_height > canvas_height 
                if axe == 'x': return content_width > canvas_width 
        
        return False
