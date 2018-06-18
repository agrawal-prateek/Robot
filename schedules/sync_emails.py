import json
import os
import re

import apiclient
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
    except apiclient.errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_message_id(service, user_id='me', query=''):
    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])
        messages_id = []
        for message in messages:
            messages_id.append(message['id'])
        return messages_id
    except apiclient.errors.HttpError as error:
        print(error)


def get_gmail_service():
    store = file.Storage('/home/pi/Robot/src/credentials/authenticated/gmail/credentials.json')
    creds = store.get()
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service


def get_email(query=''):
    service = get_gmail_service()
    messgae_ids = get_message_id(service=service, query=query)
    emails = []
    for msg_id in messgae_ids:
        try:
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
            print(n_e)
        except Exception as e:
            print(e)
            continue
    return emails


if __name__ == '__main__':
    emails_list = get_email('digitalocean')

    if not os.path.exists('/home/pi/data'):
        os.mkdir('/home/pi/data')
    with open('/home/pi/data/emails.json', 'w+') as jsonfile:
        jsonfile.write(json.dumps(emails_list))
