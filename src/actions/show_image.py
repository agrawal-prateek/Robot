from tkinter import *

from PIL import ImageTk, Image


def show_image(image_url):
    root = Tk()
    root.attributes('-fullscreen', True)
    root.bind('<Escape>', exit)
    img = ImageTk.PhotoImage(Image.open(image_url))
    panel = Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()
