import tkinter as tk
from tkinter import Tk, Label, Entry

from PIL import Image, ImageTk, ImageDraw

CURRENT_MODE = 'fill'

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
width, height = image.size
draw_frame.config(bg="#444444")

image_ = ImageTk.PhotoImage(height=image.height, width=image.width, image=image)
draw_frame.image = image_
draw_frame.config(image=image_)

def replace_rounding_pixels(x, y, color):
    m_pixel = None
    u_pixel = None
    l_pixel = None
    b_pixel = None
    r_pixel = None
    if 0 <= x < width and 0 <= y < height: m_pixel  = image.getpixel((x, y))
    if 0 <= x < width and 0 <= y+1 < height: u_pixel = image.getpixel((x, y+1))
    if 0 <= x-1 < width and 0 <= y < height: l_pixel = image.getpixel((x-1, y))
    if 0 <= x < width and 0 <= y-1 < height: b_pixel = image.getpixel((x, y-1))
    if 0 <= x+1 < width and 0 <= y < height: r_pixel = image.getpixel((x+1, y))
    if m_pixel and m_pixel != color: # mid pixel
        image.putpixel((x, y), color)
    if u_pixel and (u_pixel == m_pixel) and (u_pixel != color): # upper middle pixel
        replace_rounding_pixels(x, y+1, color)
    if l_pixel and (l_pixel == m_pixel) and (l_pixel != color): # middle left pixel
        replace_rounding_pixels(x-1, y, color)
    if b_pixel and (b_pixel == m_pixel) and (b_pixel != color): # bottom middle pixel
        replace_rounding_pixels(x, y-1, color)
    if r_pixel and (r_pixel == m_pixel) and (r_pixel != color): # middle right pixel
        replace_rounding_pixels(x+1, y, color)

def flood_fill(x, y, new_color):
    width, height = image.size
    if not (0 <= x < width and 0 <= y < height): return
    target_color = image.getpixel((x, y))

    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        cx, cy = stack.pop()

        if not (0 <= cx < width and 0 <= cy < height):
            continue

        if image.getpixel((cx, cy)) != target_color:
            continue

        image.putpixel((cx, cy), new_color)

        stack.append((cx + 1, cy))
        stack.append((cx - 1, cy))
        stack.append((cx, cy + 1))
        stack.append((cx, cy - 1))

def on_click(event):

    R = int(r_entry.get())
    G = int(g_entry.get())
    B = int(b_entry.get())
    x = event.x
    y = event.y
    if CURRENT_MODE == 'pen':
        pen_size = int(pen_size_entry.get())

        if pen_size == 1:
            image.putpixel((x, y), (R, G, B))
        elif pen_size > 1:
            draw = ImageDraw.Draw(image)

            half_size = pen_size // 2
            draw.ellipse([x - half_size, y - half_size, x + half_size, y + half_size], fill=(R, G, B))
    elif CURRENT_MODE == 'fill':
        #flood_fill(x, y, (R, G, B))
        ImageDraw.floodfill(image, (x, y), (R, G, B))

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