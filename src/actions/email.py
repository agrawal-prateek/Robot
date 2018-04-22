from __future__ import print_function

import base64
import os
from email.mime.text import MIMEText

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file

from src.auth import gmail

home_dir = os.path.expanduser('~')


def sendmail(sender, to, subject, body):
    store = file.Storage(os.path.join(home_dir, '.linuxAI', '.credentials', 'gmail', 'credentials.json'))
    creds = store.get()
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    create_message = {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('utf-8')}

    sendmessage = (service.users().messages().send(userId="me", body=create_message).execute())
    print('Message Id: %s' % sendmessage['id'])


def sendmailui():
    if not os.path.exists(os.path.join(home_dir, '.linuxAI', '.credentials', 'gmail', 'credentials.json')):
        gmail.authenticate()
