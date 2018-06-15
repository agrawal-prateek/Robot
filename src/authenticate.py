from __future__ import print_function

import os

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

home_dir = os.path.expanduser('~')


def authenticate_gmail():
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.insert',
        'https://www.googleapis.com/auth/gmail.labels',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.settings.basic',
        'https://www.googleapis.com/auth/gmail.settings.sharing',
        'https://mail.google.com/'
    ]
    if not os.path.exists(home_dir + '/Robot/src/credentials/authenticated/gmail'):
        os.mkdir(home_dir + '/Robot/src/credentials/authenticated/gmail')
    store = file.Storage(os.path.join('/home/pi/Robot/src/credentials/authenticated/gmail', 'credentials.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(home_dir + '/Robot/src/credentials/auth2/client_secret.json',
                                              SCOPES)
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


def authenticate_photos():
    SCOPES = [
        'https://www.googleapis.com/auth/photoslibrary'
    ]
    if not os.path.exists(home_dir + '/Robot/src/credentials/authenticated/photos'):
        os.mkdir(home_dir + '/Robot/src/credentials/authenticated/photos')
    store = file.Storage(os.path.join(home_dir + '/Robot/src/credentials/authenticated/photos', 'credentials.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(home_dir + '/Robot/src/credentials/auth2/client_secret.json',
                                              SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('photos', 'v1', http=creds.authorize(Http()))
