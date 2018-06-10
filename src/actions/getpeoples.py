from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def get_peoples():
    SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
    store = file.Storage('/home/pi/Robot/src/credentials/authenticated/people/credentials.json')
    creds = store.get()
    service = build('people', 'v1', http=creds.authorize(Http()))
    results = service.people().connections().list(resourceName='people/me',
                                                  personFields='names,emailAddresses,phoneNumbers').execute()
    connections = results.get('connections', [])
    peoples = []

    for person in connections:
        try:
            name = person['names'][0].get('displayName')
            phone = person['phoneNumbers'][0]['canonicalForm']
            peoples.append(
                {
                    'name': name.lower(),
                    'phone': phone
                }
            )
        except KeyError:
            pass
    return peoples