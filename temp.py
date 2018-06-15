import pprint

from googleapiclient.discovery import build


def main():
    service = build("customsearch", "v1", developerKey="AIzaSyAIUKy0S4IavWzn0OLjr6LciDHJzNzWlRw")

    res = service.cse().list(
        q='horses',
        cx='017576662512468239146:omuauf_lfve',
    ).execute()
    pprint.pprint(res)


if __name__ == '__main__':
    main()
