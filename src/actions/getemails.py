import os
import re

from apiclient import errors
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file


def get_message(service, user_id='me', msg_id=None):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
        headers = message['payload']['headers']
        for header in headers:
            if header['name'] == 'From':
                return header['value']
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_message_id(service=None, query='', max_results=1000):
    user_id = 'me'

    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query, maxResults=max_results).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        messages_id = []
        for message in messages:
            messages_id.append(message['id'])
        return messages_id
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_gmail_service():
    store = file.Storage(os.path.join('/home/pi/Robot/src/credentials/authenticated/gmail', 'credentials.json'))
    creds = store.get()
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service


def get_emails(max_results=1000, q=''):
    service = get_gmail_service()
    messgae_ids = get_message_id(service=service, query=q, max_results=max_results)
    emails = []
    for msg_id in messgae_ids:
        n_e = get_message(service=service, msg_id=msg_id)
        span = re.search('<(.*)>', n_e).span()
        email_start = span[0] + 1
        email_end = span[1] - 1
        name_start = 0
        name_end = span[0] - 1
        emails.append({
            "name": n_e[name_start:name_end],
            "email": n_e[email_start:email_end]
        })

    return emails