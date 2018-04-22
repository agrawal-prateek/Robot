from __future__ import print_function

import os

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def authenticate():
    home_dir = os.path.expanduser('~')
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.insert',
        'https://www.googleapis.com/auth/gmail.labels',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.metadata',
        'https://www.googleapis.com/auth/gmail.settings.basic',
        'https://www.googleapis.com/auth/gmail.settings.sharing',
        'https://mail.google.com/'
    ]
    if not os.path.exists(os.path.join(home_dir, '.linuxAI', '.credentials')):
        os.mkdir(os.path.join(home_dir, '.linuxAI', '.credentials'))
        os.mkdir(os.path.join(home_dir, '.linuxAI', '.credentials', 'gmail'))
    if not os.path.exists(os.path.join(home_dir, '.linuxAI', '.credentials', 'gmail')):
        os.mkdir(os.path.join(home_dir, '.linuxAI', '.credentials', 'gmail'))
    if os.path.exists(os.path.join(home_dir, '.linuxAI', '.credentials', 'gmail', 'credentials.json')):
        os.remove(os.path.join(home_dir, '.linuxAI', '.credentials', 'gmail', 'credentials.json'))

    store = file.Storage(os.path.join(home_dir, '.linuxAI', '.credentials', 'gmail', 'credentials.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('src/credentials/auth2/client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])