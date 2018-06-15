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


class ImageLabel(Label):
    """a label that displays images, and plays them if they are gifs"""

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in range(100):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 10

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def show_progressbar():
    image_url = '/home/pi/Robot/src/static/images/amc_loading#191919.gif'
    root = Tk()
    root.attributes('-fullscreen', True)
    root.bind('<Escape>', exit)
    lbl = ImageLabel(root)
    lbl.configure(background='#191919')
    lbl.pack(side="bottom", fill="both", expand="yes")
    lbl.load(image_url)
    root.mainloop()
