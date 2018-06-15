import os
from tkinter import *
import time
import sys
sys.path.append('/home/pi/Robot')

from src.actions import nlp


def start_timer_subprocess(query):
    class Timer:
        def __init__(self, hour, minute, sec):
            self.root = Tk()
            self.hour = hour
            self.minute = minute
            self.sec = sec
            self.main_hour = hour
            self.main_minute = minute
            self.main_sec = sec
            self.root.attributes('-fullscreen', True)
            self.root.bind('<Escape>', exit)
            self.frame = Frame(self.root)
            self.time = Label(
                self.frame,
                text=str(self.hour) + ' : ' + str(self.minute) + ' : ' + str(self.sec),
                font=('Helvetica', 88)
            )
            self.frame.pack(expand=True)
            self.time.pack()
            self.start_timer()

        def update_time(self):
            self.sec -= 1
            if self.sec < 0:
                self.sec = 59
                self.minute -= 1
            if self.minute < 0:
                self.hour -= 1
                self.minute = 59
            self.time['text'] = str(self.hour) + ' : ' + str(self.minute) + ' : ' + str(self.sec)
            self.time.update()

        def alarm(self):
            text = "/home/pi/Robot/src/speaktext.sh '"
            if self.main_hour != 0:
                text += str(self.main_hour) + " hour "
            if self.main_minute != 0:
                text += str(self.main_minute) + " minute "
            if self.main_sec != 0:
                text += str(self.main_sec) + " second "
            text += "has been finished!'"
            os.system(text)

        def run_timer(self):
            while True:
                self.update_time()
                if self.hour == 0 and self.minute == 0 and self.sec == 0:
                    self.alarm()
                    self.root.destroy()
                time.sleep(0.99)

        def start_timer(self):
            self.root.after(1000, self.run_timer)
            self.root.mainloop()

    h = 0
    m = 0
    s = 0
    h_m_s = []
    data = nlp.get_parts_of_speech(query)
    for part in data:
        if part['parts_of_speech'] == 'NUM':
            h_m_s.append(part['token'])
        elif part['parts_of_speech'] == 'NOUN':
            if part['token'] == 'seconds' or \
                    part['token'] == 'second' or \
                    part['token'] == 'hour' or \
                    part['token'] == 'hours' or \
                    part['token'] == 'minutes' or \
                    part['token'] == 'minute':
                h_m_s.append(part['token'])
    for i in range(1, len(h_m_s)):
        if h_m_s[i] == 'second' or h_m_s[i] == 'seconds':
            s = int(h_m_s[i - 1])
        if h_m_s[i] == 'minute' or h_m_s[i] == 'minutes':
            m = int(h_m_s[i - 1])
        if h_m_s[i] == 'hour' or h_m_s[i] == 'hours':
            h = int(h_m_s[i - 1])
    if not h and not s and not m:
        os.system('mpg123 /home/pi/Robot/src/audio/pleaseTellMeTheDurationOfTime.mp3')
        return
    Timer(hour=h, minute=m, sec=s)


if __name__ == '__main__':
    start_timer_subprocess(sys.argv[1])
