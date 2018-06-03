from __future__ import print_function

import base64
import os
import time
from email.mime.text import MIMEText
from tkinter import *
import sys
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file

from src.auth import gmail

home_dir = os.path.expanduser('~')
root = None
e1, e2, e3, e4, errormessage = None, None, None, None, None


def destroy(*args):
    global root
    root.destroy()


def sendmail():
    global e1, e2, e3, e4, errormessage
    try:
        store = file.Storage(home_dir + '/Robot/src/credentials/authenticated/gmail/credentials.json')
        creds = store.get()
        service = build('gmail', 'v1', http=creds.authorize(Http()))

        message = MIMEText(e4.get("1.0", END))
        message['to'] = e2.get()
        message['from'] = e1.get()
        message['subject'] = e3.get()
        create_message = {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('utf-8')}

        sendmessage = (service.users().messages().send(userId="me", body=create_message).execute())
        print('Message Id: %s' % sendmessage['id'])
        errormessage.config(fg='green')
        errormessage['text'] = 'Message sent Successfully!'
        time.sleep(2)
        destroy()
    except Exception as e:
        print(e)
        errormessage.config(fg='red')
        errormessage['text'] = 'Sorry, Message could not sent! Please check your details'


def sendmailui():
    global root, e1, e2, e3, e4, errormessage
    if not os.path.exists(os.path.join(home_dir + '/Robot/src/credentials/authenticated/gmail', 'credentials.json')):
        gmail.authenticate()

    root = Tk()
    root.title('Send Email')
    root.geometry('813x413+276+177')
    root.config(bg='#fff')
    f = Frame(root, bd=0, bg='#fff')
    f.grid(padx=15, pady=15)
    l1 = Label(f, text='From:', font='"Roboto Mono" 12 bold', bd=0, bg='#fff', width=25)
    l1.grid(row=1, column=1)
    e1 = Entry(f, bd=0, width=50, x=30)
    e1.grid(row=1, column=2)
    l2 = Label(f, text='To:', font='"Roboto Mono" 12 bold', bd=0, bg='#fff', width=25, height=3)
    l2.grid(row=2, column=1)
    e2 = Entry(f, bd=0, width=50, x=30)
    e2.grid(row=2, column=2)
    l3 = Label(f, text='Subject:', font='"Roboto Mono" 12 bold', bd=0, bg='#fff', width=25, height=3)
    l3.grid(row=3, column=1)
    e3 = Entry(f, bd=0, width=50, x=30)
    e3.grid(row=3, column=2)
    l4 = Label(f, text='Message:', font='"Roboto Mono" 12 bold', bd=0, bg='#fff', width=25)
    l4.grid(row=4, column=1)
    e4 = Text(f, bd=0, width=57, height=10)
    e4.grid(row=4, column=2)
    scrollb = Scrollbar(f, command=e4.yview)
    scrollb.grid(row=4, column=3, sticky='nsew')
    e4['yscrollcommand'] = scrollb.set
    f1 = Frame(root, bd=0, bg='#fff')
    f1.grid(padx=15, pady=15)
    b1 = Button(f1, text="Cancel", width=10, command=destroy)
    b1.grid(row=1, column=1, padx=60)
    b2 = Button(f1, text="Send Email", width=10, command=sendmail)
    b2.grid(row=1, column=2)
    errormessage = Label(f1, text='', bd=0, bg='#fff', fg='#50ff50')
    errormessage.grid(row=2, column=1)
    root.bind('<Escape>', destroy)
    root.mainloop()


def send_message(query):
    pass


def send_email(query):
    pass
