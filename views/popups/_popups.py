import customtkinter as ctk
from ImageModules import Modify
from customtkinter import CTkFrame, CTkLabel, CTkImage, RIGHT, BOTH, BOTTOM, LEFT, X
from PIL import Image

class EditPopup(ctk.CTkToplevel):
    def __init__(self, master, image):
        super().__init__(master)
        self.title("Edit Image")
        self.geometry("600x600")
        self.resizable(False, False)
        self.transient(master)  # Keep the popup on top of the master window
        self.grab_set()  # Make the popup modal

        self.image = image
        self.rotate_image = image.copy()

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.configure(fg_color="transparent")
        self.buttons_frame.pack(side=LEFT, pady=5, padx=5)

        self.bw_frame = ctk.CTkFrame(self.buttons_frame)
        self.bw_frame.configure(border_width=1, border_color="gray", corner_radius=10, fg_color="transparent")
        self.bw_frame.pack(pady=10)
        self.bw_button = ctk.CTkButton(self.bw_frame, text="Black & White", command=self.BlackandWhite_image)
        self.bw_button.pack(pady=5, padx=5)

        self.resize_frame = ctk.CTkFrame(self.buttons_frame)
        self.resize_frame.configure(border_width=1, border_color="gray", corner_radius=10, fg_color="transparent")
        self.resize_frame.pack(pady=10)
        self.resize_x_input = ctk.CTkEntry(self.resize_frame, placeholder_text="Width")
        self.resize_x_input.pack(pady=5, padx=10)
        self.resize_y_input = ctk.CTkEntry(self.resize_frame, placeholder_text="Height")
        self.resize_y_input.pack(pady=5, padx=10)
        self.resize_button = ctk.CTkButton(self.resize_frame, text="Resize", command=self.Resize_image)
        self.resize_button.pack(pady=5, padx=10)

        self.brightness_frame = ctk.CTkFrame(self.buttons_frame)
        self.brightness_frame.configure(border_width=1, border_color="gray", corner_radius=10, fg_color="transparent")
        self.brightness_frame.pack(pady=10)
        self.brightness_input= ctk.CTkEntry(self.brightness_frame, placeholder_text="Intensity")
        self.brightness_input.pack(pady=5, padx=10)
        self.resize_button = ctk.CTkButton(self.brightness_frame, text="Change Brightness", command=self.Brightness_image)
        self.resize_button.pack(pady=5, padx=10)

        self.rotation_frame = ctk.CTkFrame(self.buttons_frame)
        self.rotation_frame.configure(border_width=1, border_color="gray", corner_radius=10, fg_color="transparent")
        self.rotation_frame.pack(pady=10, padx=10)
        self.rotation_input= ctk.CTkEntry(self.rotation_frame, placeholder_text="Angle")
        self.rotation_input.pack(pady=5, padx=10)
        self.resize_button = ctk.CTkButton(self.rotation_frame, text="Rotate", command=self.Rotate_image)
        self.resize_button.pack(pady=5, padx=10)

        self.photo_frame = _PhotoFrame(self, 300, 300)
        self.photo_frame.pack(side=RIGHT, pady=5, padx=5)

        self.apply_button = ctk.CTkButton(self, text="Apply Changes", command=self.apply)
        self.apply_button.pack(side=BOTTOM, fill=X, pady=10, padx=10)

    def apply(self):
        self.master.photo_frame.update_display(self.image)
        self.destroy()

    def BlackandWhite_image(self):
        self.rotate_image = Modify.BlackandWhiteImage(self.image)
        self.image = Modify.BlackandWhiteImage(self.image)
        self.photo_frame.update_display()

    def Resize_image(self):
        if self.resize_x_input.get() == "" or self.resize_y_input.get() == "":
            return
        self.rotate_image = Modify.ReSizeImage(self.image, (int(self.resize_x_input.get()), int(self.resize_y_input.get())))
        self.image = Modify.ReSizeImage(self.image, (int(self.resize_x_input.get()), int(self.resize_y_input.get())))
        self.photo_frame.update_display()

    def Brightness_image(self):
        if self.brightness_input.get() == "":
            return
        self.rotate_image = Modify.BrightnessImage(self.image, float(self.brightness_input.get()))
        self.image = Modify.BrightnessImage(self.image, float(self.brightness_input.get()))
        self.photo_frame.update_display()
    
    def Rotate_image(self):
        if self.rotation_input.get() == "":
            return
        self.image = Modify.RotateImage(self.rotate_image, float(self.rotation_input.get()))
        self.photo_frame.update_display()

    def get_image(self):
        return self.image

class CropPopup(ctk.CTkToplevel):
    def __init__(self, master, image):
        super().__init__(master)
        self.title("Crop Image")
        self.geometry("600x600")
        self.resizable(False, False)
        self.transient(master)  # Keep the popup on top of the master window
        self.grab_set()  # Make the popup modal

        self.image = image
        self.original_image = image.copy()

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.configure(fg_color="transparent")
        self.buttons_frame.pack(side=LEFT, pady=5, padx=5)

        self.top_frame = ctk.CTkFrame(self.buttons_frame)
        self.top_frame.configure(border_width=1, border_color="gray", corner_radius=10, fg_color="transparent")
        self.top_frame.pack(pady=10)
        self.top_label = ctk.CTkLabel(self.top_frame, text="Top")
        self.top_label.pack(pady=5, padx=5)
        self.top_input = ctk.CTkEntry(self.top_frame, placeholder_text="Top")
        self.top_input.insert(0, "0")
        self.top_input.bind("<Return>", lambda event: self.Crop_image())
        self.top_input.pack(pady=5, padx=10)

        self.left_frame = ctk.CTkFrame(self.buttons_frame)
        self.left_frame.configure(border_width=1, border_color="gray", corner_radius=10, fg_color="transparent")
        self.left_frame.pack(pady=10)
        self.left_label = ctk.CTkLabel(self.left_frame, text="Left")
        self.left_label.pack(pady=5, padx=5)
        self.left_input = ctk.CTkEntry(self.left_frame, placeholder_text="Left")
        self.left_input.insert(0, "0")
        self.left_input.bind("<Return>", lambda event: self.Crop_image())
        self.left_input.pack(pady=5, padx=10)

        self.bottom_frame = ctk.CTkFrame(self.buttons_frame)
        self.bottom_frame.configure(border_width=1, border_color="gray", corner_radius=10, fg_color="transparent")
        self.bottom_frame.pack(pady=10)
        self.bottom_label = ctk.CTkLabel(self.bottom_frame, text="Bottom")
        self.bottom_label.pack(pady=5, padx=5)
        self.bottom_input = ctk.CTkEntry(self.bottom_frame, placeholder_text="Bottom")
        self.bottom_input.insert(0, str(self.image.height))
        self.bottom_input.bind("<Return>", lambda event: self.Crop_image())
        self.bottom_input.pack(pady=5, padx=10)

        self.right_frame = ctk.CTkFrame(self.buttons_frame)
        self.right_frame.configure(border_width=1, border_color="gray", corner_radius=10, fg_color="transparent")
        self.right_frame.pack(pady=10)
        self.right_label = ctk.CTkLabel(self.right_frame, text="Right")
        self.right_label.pack(pady=5, padx=5)
        self.right_input = ctk.CTkEntry(self.right_frame, placeholder_text="Right")
        self.right_input.insert(0, str(self.image.width))
        self.right_input.bind("<Return>", lambda event: self.Crop_image())
        self.right_input.pack(pady=5, padx=10)
        
        self.crop_button = ctk.CTkButton(self.buttons_frame, text="Crop", command=self.Crop_image)
        self.crop_button.pack(pady=5, padx=5)

        self.reset_button = ctk.CTkButton(self.buttons_frame, fg_color="red", text="Reset", command=self.reset)
        self.reset_button.pack(pady=5, padx=5)

        self.apply_button = ctk.CTkButton(self.buttons_frame, text="Apply Changes", command=self.apply)
        self.apply_button.pack(pady=5, padx=5)

        height = self.image.height
        width = self.image.width
        if height > 400:
            ratio = 400 / height
            height = 400
            width = int(width * ratio)
        if width > 400:
            ratio = 400 / width
            width = 400
            height = int(height * ratio)
        self.geometry(f"{width + 200}x{self.winfo_height()}")
        
        self.photo_frame = _PhotoFrame(self, width, height)
        self.photo_frame.pack(fill=BOTH, expand=True)
    
    def Crop_image(self):
        if self.top_input.get() == "": self.top_input.insert(0, "0")
        if self.left_input.get() == "": self.left_input.insert(0, "0")
        if self.bottom_input.get() == "": self.bottom_input.insert(0, str(self.image.height))
        if self.right_input.get() == "": self.right_input.insert(0, str(self.image.width))
        box = (int(self.left_input.get()), int(self.top_input.get()),
               int(self.right_input.get()), int(self.bottom_input.get()))
        self.image = Modify.CropImage(self.original_image, box)
        self.photo_frame.update_display()

    def reset(self):
        self.image = self.original_image

        self.top_input.delete(0, 'end')
        self.top_input.insert(0, "0")
        self.left_input.delete(0, 'end')
        self.left_input.insert(0, "0")
        self.bottom_input.delete(0, 'end')
        self.bottom_input.insert(0, str(self.image.height))
        self.right_input.delete(0, 'end')
        self.right_input.insert(0, str(self.image.width))

        self.photo_frame.update_display()

    def get_image(self):
        return self.image
    
    def apply(self):
        self.master.photo_frame.update_display(self.image)
        self.destroy()

class _PhotoFrame(CTkFrame):
    def __init__(self, master, width=None, height=None):
        super().__init__(master)
        self.image_pil: Image.Image = None
        self.image_ctk = None
        self.asset_path = None

        self.width = width
        self.height = height

        self.image_label = CTkLabel(self, text="Aucune image chargée")
        self.image_label.pack(fill=BOTH, expand=True)

        self.update_display()
    
    def update_display(self):

        self.image_pil = self.master.get_image()

        if self.image_pil is None:
            self.image_label.configure(text="Aucune image chargée", image=None)
            return
        
        width = self.width or self.image_pil.width
        height = self.height or self.image_pil.height

        try:
            temp_image = self.image_pil.copy()
            self.image_ctk = CTkImage(temp_image, size=(width, height))
            self.image_label.configure(image=self.image_ctk, text="")

        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'affichage: {e}")