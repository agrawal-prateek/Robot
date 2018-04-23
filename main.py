#!/usr/bin/env python

from tkinter import *

from src.actions import openapplication, email
from src.grpc import pushtotalk


def runapp():
    query = None
    try:
        query = pushtotalk.main()
    except Exception as e:
        print(e)
    if re.search('open(.*)', query):
        openapplication.openapp(re.search('open(.*)', query).group(1))
    elif re.search('(.*)send(.*)email(.*)', query):
        email.sendmailui()


approot = Tk()
approot.title('LinuxAI')
approot.config(bg='#000', bd=0)

photo1 = PhotoImage(file='src/static/artificial_intelligence.gif', format='gif -index 1')
label = Label(approot, image=photo1, bd=0, bg='#000')
label.pack(fill=BOTH)

appb2 = Button(approot, text="Run", width=10, command=runapp, bg='#fff')
appb2.pack()
templabel = Label(approot, fg='#000', bg='#000')
templabel.pack()
approot.bind('<Escape>', exit)
approot.resizable(False, False)
approot.mainloop()
