from __future__ import print_function

import base64
import os
import re
from email.mime.text import MIMEText

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file
from twilio.rest import Client

from schedules import sync_peoples
from src.actions import speech_to_text


def sendmail(to_address, subject, email_text):
    from_address = 'prateekagrawal89760@gmail.com'
    try:
        store = file.Storage('/home/pi/Robot/src/credentials/authenticated/gmail/credentials.json')
        creds = store.get()
        service = build('gmail', 'v1', http=creds.authorize(Http()))

        message = MIMEText(email_text)
        message['to'] = to_address
        message['from'] = from_address
        message['subject'] = subject
        create_message = {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('utf-8')}

        sendmessage = (service.users().messages().send(userId="me", body=create_message).execute())
        print('Message Id: %s' % sendmessage['id'])
    except Exception as e:
        print(e)


def send_message():
    persons = sync_peoples.get_peoples()
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


def send_email():
    os.system("mpg123 /home/pi/Robot/src/audio/telltheemailoftheperson.mp3")
    while True:
        initial_email = speech_to_text.get_user_input()
        print(initial_email)
        if not re.search('(.+)@(.+).(.+)', initial_email):
            os.system('mpg123 /home/pi/Robot/src/audio/pleasetellthevalidemail.mp3')
        else:
            break
    email = ''
    for i in initial_email:
        if i != ' ':
            email += i

    os.system('mpg123 /home/pi/Robot/src/audio/whatsYourMessage.mp3')
    message = speech_to_text.get_user_input()

    os.system('mpg123 /home/pi/Robot/src/audio/tellTheSubject.mp3')
    subject = speech_to_text.get_user_input()

    sendmail(
        to_address=email,
        subject=subject,
        email_text=message
    )
    os.system('mpg123 /home/pi/Robot/src/audio/emailSentSuccessfully.mp3')
