from tkinter import filedialog
from PIL import Image

def save_image_as(image: Image.Image):
    '''Opens a file dialog to save the given image with user-specified name and format.'''
    filestypes = [
            ("Joint Photographic Experts Group", "*.jpeg; *.jpg"),
            ("Portable Network Graphic", "*.png"),
            ]
    fp = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filestypes)
    if not fp: # User cancelled the dialog
        return
    image.save(fp=fp)

def save_text_as(text: str):
    '''Opens a file dialog to save the given text with user-specified name.'''
    filestypes = [
            ("Text File", "*.txt"),
            ]
    fp = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=filestypes)
    if not fp: # User cancelled the dialog
        return
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)