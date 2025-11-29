import os
from customtkinter import *
import json
from PIL import Image, ImageTk
# from hPyT import title_bar_color
import time
import sys
import ImageModules
from popups import CropPopup, EditPopup

with open(os.path.join(os.path.dirname(__file__), "settings.json"), "r") as f:
    read = f.read()
    settings = json.loads(read)

class TopBarApp(CTkFrame):
    ''' Top Bar of the App. '''
    def __init__(self, master):
        super().__init__(master)

        self.configure(height=40)

        self.menu = self.Menu(self)
        self.menu.pack(side=LEFT, padx=5, pady=5)

        self.menu = self.ActionsHandler(self)
        self.menu.pack(side=LEFT, padx=5, pady=5)

        self.menu = self.ImageImport(self)
        self.menu.pack(side=LEFT, padx=5, pady=5)

        self.menu = self.Zoom(self)
        self.menu.pack(side=LEFT, padx=5, pady=5)

        self.edit = self.Edit(self)
        self.edit.pack(side=LEFT, padx=5, pady=5)

        self.crop = self.Crop(self)
        self.crop.pack(side=LEFT, padx=5, pady=5)

        self.search_bar = self.SearchBar(self)
        self.search_bar.pack(padx=5, pady=5)

        self.pack(fill=X, padx=5, pady=(5, 0))

    class SearchBar(CTkFrame):
        def __init__(self, master):
            super().__init__(master)

            self.configure(corner_radius=0, fg_color="transparent")

            self.search_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "search.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "search.png")), (20, 20))

            self.search_button = CTkButton(self, image=self.search_image, text="", width=30, height=30, fg_color="transparent", command=self.search)
            self.search_input = self.SearchInput(self)

            self.search_input.grid(row=0, column=0)
            self.search_button.grid(row=0, column=1)

        def search(self):
            '''' Perform search action. '''
            query = self.search_input.search_entry.get()
            if query.startswith('/'):
                split_query = query.split(' ')
                match split_query[0]:
                    case '/state':
                        print(f"Previous state: {self.master.master.state()}")
                        if split_query[1] == 'normal':
                            self.master.master.state('normal')
                        elif split_query[1] == 'zoomed':
                            self.master.master.state('zoomed')
                        print(f"Current state: {self.master.master.state()}")
                    case '/color-theme':
                        if split_query[1] in ['blue', 'dark-blue', 'green']:
                            set_default_color_theme(split_query[1])
                            settings["color-theme"] = split_query[1]
                    case '/appearance':
                        if split_query[1] in ['System', 'Dark', 'Light']:
                            set_appearance_mode(split_query[1])
                            settings["appearance"] = split_query[1]
                    case '/restart':
                        self.master.master.restart()

        class SearchInput(CTkFrame):
            ''' Search input field with clear button. '''
            def __init__(self, master):
                super().__init__(master)

                self.configure(corner_radius=0, fg_color="transparent")

                self.clear_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "cross.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "cross.png")), (20, 20))

                self.search_entry = CTkEntry(self, placeholder_text="Search...", width=200, height=30, border_width=1, corner_radius=10, fg_color="transparent", border_color="#1D1D1D" if get_appearance_mode() == "Light" else "#DDDDDD", text_color="#000000" if get_appearance_mode() == "Light" else "#FFFFFF", font=("Arial", 14))
                self.search_entry.bind("<Return>", lambda event: self.master.search())
                self.search_entry.pack(side=LEFT, fill="x", expand=True, padx=5)
                
                self.clear_button = CTkButton(self, image=self.clear_image, text="", width=30, height=30, fg_color="transparent", command=lambda: self.search_entry.delete(0, 'end'))
                self.clear_button.pack(side=RIGHT)

    class Menu(CTkFrame):
        ''' App menu. '''
        def __init__(self, master):
            super().__init__(master)

            self.configure(corner_radius=0, fg_color="transparent")

            self.menu_frame = MenuFrame(self.master.master)

            self.menu_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "options.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "options.png")), (20, 20))
            self.menu_button = CTkButton(self, image=self.menu_image, text="", width=30, height=30, fg_color="transparent", command=self.menu_frame.open_menu)
            self.menu_button.pack()

    class ActionsHandler(CTkFrame):
        ''' Functions to redo. '''
        def __init__(self, master):
            super().__init__(master)

            self.configure(height=40, fg_color="transparent")

            self.redo_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "redo.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "redo.png")), (20, 20))
            self.undo_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "undo.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "undo.png")), (20, 20))

            self.redo_button = CTkButton(self, image=self.redo_image, text="", width=30, height=30, fg_color="transparent", command=self.redo)
            self.undo_button = CTkButton(self, image=self.undo_image, text="", width=30, height=30, fg_color="transparent", command=self.undo)
            
            self.undo_button.grid(row=0, column=0)
            self.redo_button.grid(row=0, column=1)

        def redo(self):
            ''' Redo the last action. '''
            pass

        def undo(self):
            ''' Undo the last action. '''
            pass

    class ImageImport(CTkFrame):
        def __init__(self, master):
            super().__init__(master)

            self.configure(height=40, fg_color="transparent")

            self.import_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "open-folder.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "open-folder.png")), (20, 20))
            self.save_as_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "save.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "save.png")), (20, 20))

            self.import_button = CTkButton(self, image=self.import_image, text="", width=30, height=30, fg_color="transparent", command=lambda: master.master.photo_frame.set())
            self.save_as_button = CTkButton(self, image=self.save_as_image, text="", width=30, height=30, fg_color="transparent", command=lambda: ImageModules.File.save_as(master.master.photo_frame.get_image()))
            
            self.import_button.grid(row=0, column=0)
            self.save_as_button.grid(row=0, column=1)
    
    class Zoom(CTkFrame):
        def __init__(self, master):
            super().__init__(master)

            self.configure(height=40, fg_color="transparent")

            self.zoom_out_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "zoom-in.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "zoom-in.png")), (20, 20))
            self.zoom_in_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "zoom-out.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "zoom-out.png")), (20, 20))

            self.zoom_out_button = CTkButton(self, image=self.zoom_out_image, text="", width=30, height=30, fg_color="transparent", command=lambda: master.master.photo_frame.increment_zoom(0.1))
            self.zoom_in_button = CTkButton(self, image=self.zoom_in_image, text="", width=30, height=30, fg_color="transparent", command=lambda: master.master.photo_frame.increment_zoom(-0.1))
            
            self.zoom_out_button.grid(row=0, column=0)
            self.zoom_in_button.grid(row=0, column=1)
    
    class Edit(CTkFrame):
        def __init__(self, master):
            super().__init__(master)

            self.configure(height=40, fg_color="transparent")
            self.edit_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "edit.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "edit.png")), (20, 20))
            self.edit_button = CTkButton(self, image=self.edit_image, text="", width=30, height=30, fg_color="transparent", command=self.open_edit_popup)
            self.edit_button.pack()

        def open_edit_popup(self):
            ''' Open the edit popup window. '''
            EditPopup(self.master.master, self.master.master.photo_frame.get_image())

    class Crop(CTkFrame):
        def __init__(self, master):
            super().__init__(master)

            self.configure(height=40, fg_color="transparent")
            self.crop_image = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "img_dark", "crop.png")), Image.open(os.path.join(os.path.dirname(__file__), "img_light", "crop.png")), (20, 20))
            self.crop_button = CTkButton(self, image=self.crop_image, text="", width=30, height=30, fg_color="transparent", command=self.open_crop_popup)
            self.crop_button.pack()

        def open_crop_popup(self):
            ''' Crop the current image. '''
            CropPopup(self.master.master, self.master.master.photo_frame.get_image())

class PhotoFrame(CTkFrame):
    ''' Frame to display video content with scrollbars and mouse navigation. '''
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=True, pady=5, padx=5)
        
        self.zoom = 0.5
        self.image_pil = None
        self.image_ctk = None
        self.asset_path = None

        self.yscroll_bar = CTkScrollbar(self, orientation=VERTICAL)
        self.yscroll_bar.pack(fill=Y, side=RIGHT, expand=False)
        self.xscroll_bar = CTkScrollbar(self, orientation=HORIZONTAL)
        self.xscroll_bar.pack(fill=X, side=BOTTOM, expand=False)
        
        self.canvas = CTkCanvas(self, 
                                yscrollcommand=self.yscroll_bar.set, 
                                xscrollcommand=self.xscroll_bar.set,
                                bg=ThemeManager.theme["CTkFrame"]["fg_color"][1]
                                )
        self.canvas.pack(fill=BOTH, expand=True)

        self.yscroll_bar.configure(command=self.canvas.yview)
        self.xscroll_bar.configure(command=self.canvas.xview)

        self.image_label = CTkLabel(self.canvas, text="Aucune image chargée")
        self.canvas_window = self.canvas.create_window(0, 0, anchor=NW, window=self.image_label)

        self._keybinds()
    
    def mouse_wheel(self, event):
        """Gère le défilement vertical avec la molette"""
        if self._is_scrollbar_active('y'):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def alt_mouse_wheel(self, event):
        """Gère le défilement horizontal avec la molette"""
        if self._is_scrollbar_active('x'):
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def ctrl_mouse_wheel(self, event):
        """Gère la molette de souris pour le zoom (optionnel)"""
        if event.delta > 0:
            self.increment_zoom(0.1)
        else:
            self.increment_zoom(-0.1)

    def set(self, asset_path=None):
        ''' Set the image to display. '''
        self.asset_path = asset_path or filedialog.askopenfilename()
        
        if not self.asset_path:
            return
            
        try:
            self.image_pil = Image.open(self.asset_path)
            self.update_display()
            
        except Exception as e:
            self.image_label.configure(text=f"Erreur: {str(e)}")
    
    def update_display(self, image=None):
        """Met à jour l'affichage de l'image avec le zoom actuel"""
        if self.image_pil is None:
            return
        
        if image:
            self.image_pil = image
        else:
            self.image_pil = self.image_pil
        
        width = int(self.image_pil.width * self.zoom)
        height = int(self.image_pil.height * self.zoom)
        
        max_size = 5000
        if width > max_size or height > max_size:
            ratio = min(max_size / width, max_size / height)
            width = int(width * ratio)
            height = int(height * ratio)
        
        try:
            self.image_ctk = CTkImage(self.image_pil, size=(width, height))
            self.image_label.configure(image=self.image_ctk, text="", width=width, height=height)
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'affichage: {e}")
    
    def get_image(self):
        """Retourne l'image PIL actuelle"""
        return self.image_pil
    
    def change_zoom(self, zoom: float):
        """Change le zoom à une valeur spécifique"""
        if zoom > 0 and zoom <= 10:
            self.zoom = zoom
            self.update_display()
            self.after(10, self.center_image)
    
    def increment_zoom(self, zoom_delta: float):
        """Incrémente le zoom de la valeur spécifiée"""
        new_zoom = self.zoom + zoom_delta
        if 0.1 <= new_zoom <= 10:
            self.zoom = new_zoom
            self.update_display()
    
    def _keybinds(self):

        self.image_label.bind("<Control-MouseWheel>", self.ctrl_mouse_wheel)
        self.image_label.bind("<Alt-MouseWheel>", self.alt_mouse_wheel)
        self.image_label.bind("<MouseWheel>", self.mouse_wheel)

    def _is_scrollbar_active(self, axe: str ="x") -> bool:
        """Vérifie si les scrollbars sont nécessaires (l'image dépasse la taille du canvas)"""
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
    
class MenuFrame(CTkFrame):
    ''' Frame for the app menu options. '''
    def __init__(self, master):
        super().__init__(master)

        
    def open_menu(self):
        ''' Open the app menu. '''
        if self.winfo_ismapped():
            self.place_forget()
        else:
            self.place(
                x=5,
                y=50,
                relheight=1.0,
                anchor=NW
            )

            self.lift()

class App(CTk):
    ''' Main Application Class. '''
    def __init__(self):
        super().__init__()
        self.title("Photo Editor")
        self.geometry("800x600")

        set_appearance_mode(settings["appearance"])
        set_default_color_theme(settings["color-theme"])

        self.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        self.top_bar = TopBarApp(self)
        self.photo_frame = PhotoFrame(self)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<F11>", lambda event: self.toggle_fullscreen())
        
        self.after(100, self.load_settings)
        
    def load_settings(self):
        ''' Load settings from the settings.json file. '''
        if settings["geometry"]: self.geometry(settings["geometry"])
        if settings["fullscreen"]: 
            self.state("zoomed")
    
    def on_closing(self):
        ''' Save settings and close the app. '''
        if self.state() == 'zoomed':
            settings["fullscreen"] = True
            settings["geometry"] = None
        else:
            settings["fullscreen"] = False
            settings["geometry"] = self.geometry()

        settings["appearance"] = get_appearance_mode()
        with open(os.path.join(os.path.dirname(__file__), "settings.json"), "w") as f:
            f.write(json.dumps(settings, indent=4))
        self.destroy()

    def toggle_fullscreen(self):
        ''' Toggle fullscreen mode. '''
        if self.state() == 'normal':
            self.state('zoomed')
        elif self.state() == 'zoomed':
            self.state('normal')
    
    def restart(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        self.on_closing()
        time.sleep(0.5)
        python = sys.executable
        os.execl(python, python, * sys.argv)