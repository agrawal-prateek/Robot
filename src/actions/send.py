from __future__ import print_function

import base64
import os
import time
from email.mime.text import MIMEText
from tkinter import *
from src.actions import getemails

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file
from twilio.rest import Client

from src.actions import getpeoples
from src.actions import speech_to_text

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
    persons = getpeoples.get_peoples()
    print(persons)
    os.system('mpg123 /home/pi/Robot/src/audio/pleaseTellMeTheNameOfThePersonToWhomYouWantToSendMessage.mp3')
    personname = speech_to_text.get_user_input().lower()
    personphone = None
    for person in persons:
        if person['name'].find(personname) != -1:
            personphone = person['phone']
            break
    if not personphone:
        os.system('mpg123 /home/pi/Robot/src/audio/sorryICouldntFindThePersonToWhomYouWantToSendTheMessage.mp3')
        return
    os.system('mpg123 /home/pi/Robot/src/audio/whatsYourMessage.mp3')
    messagetext = speech_to_text.get_user_input()
    client = Client("AC2bb615af88faf946ecb4d1e3c013771e", "74cf75c65a2a39660f6401fbc58aa563")

    message = client.messages.create(
        body=messagetext,
        from_='+17738255252',
        to=personphone
    )

    print(message.sid)
    os.system('mpg123 /home/pi/Robot/src/audio/messagesentsuccessfully.mp3')


def send_email(query):
    # emails = getemails.get_emails(max_results=100)
    # print(emails)
    pass