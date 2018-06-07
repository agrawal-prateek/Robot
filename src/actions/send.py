from __future__ import print_function

import base64
import os
import time
from email.mime.text import MIMEText
from tkinter import *
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


def send_message(query):
    print('haha')


def send_email(query):
    pass

