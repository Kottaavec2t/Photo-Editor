import tkinter as tk
from tkinter import Tk, Label, Entry

from PIL import Image, ImageTk, ImageDraw

root = Tk()
root.title("Logiciel de retouche photo")
root.state("zoomed")
root.minsize(640, 480)

draw_frame = Label(root)

r_entry = Entry(root)
r_entry.insert(0, "R")

g_entry = Entry(root)
g_entry.insert(0, "G")

b_entry = Entry(root)
b_entry.insert(0, "B")

pen_size_entry = Entry(root)
pen_size_entry.insert(0, "pen size (pixel)")

image = Image.new("RGB", (500, 500))
draw_frame.config(bg="#444444")

image_ = ImageTk.PhotoImage(height=image.height, width=image.width, image=image)
draw_frame.image = image_
draw_frame.config(image=image_)

def on_click(event):
    
    R = int(r_entry.get())
    G = int(g_entry.get())
    B = int(b_entry.get())
    x = event.x
    y = event.y
    pen_size = int(pen_size_entry.get())

    if pen_size == 1:
        image.putpixel((x, y), (R, G, B))
    elif pen_size > 1:
        draw = ImageDraw.Draw(image)

        half_size = pen_size // 2
        draw.ellipse([x - half_size, y - half_size, x + half_size, y + half_size], fill=(R, G, B))

    image_ = ImageTk.PhotoImage(height=image.height, width=image.width, image=image)
    draw_frame.image = image_
    draw_frame.config(image=image_)
    image.save("test.png", "PNG")

draw_frame.bind("<Button-1>", on_click)

pen_size_entry.pack()
r_entry.pack()
g_entry.pack()
b_entry.pack()
draw_frame.pack()
root.mainloop()