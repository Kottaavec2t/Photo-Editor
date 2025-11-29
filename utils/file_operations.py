from tkinter import filedialog
from PIL import Image

def save_as(image: Image.Image):
    '''Opens a file dialog to save the given image with user-specified name and format.'''
    filestypes = [
            ("Joint Photographic Experts Group", "*.jpeg; *.jpg"),
            ("Portable Network Graphic", "*.png"),
            ]
    fp = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filestypes)
    image.save(fp=fp)
