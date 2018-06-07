import time


def start_timer(hour, minute, sec):
    from tkinter import Tk, Label, Frame

    def update_time():
        global hour, minute, sec
        sec, minute, hour = int(sec), int(minute), int(hour)
        sec = sec - 1
        if sec < 0:
            minute = minute - 1
            sec = 59

        if minute < 0:
            hour = hour - 1
            minute = 59
        print(sec, minute, hour)
        label.config(text=str(hour) + ":" + str(minute) + ":" + str(sec))

    def f():
        while True:
            update_time()
            time.sleep(1)

    def destroy(event):
        root.destroy()

    root = Tk()
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", destroy)

    frame = Frame(root)
    label = Label(frame, text=hour + ":" + minute + ":" + sec)
    frame.pack(expand=True)
    label.pack()
    root.after(1000, f)
    root.mainloop()


start_timer('1', '1', '3')
