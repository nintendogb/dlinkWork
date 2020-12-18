import datetime
import pickle
import json
import os.path
import redis

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

redis_url = '****************'
redis_port = *****

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
tw_tz = datetime.timezone(datetime.timedelta(hours=+8))

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/home/dlink/tool/tool/google_calendar/token.pickle'):
        with open('/home/dlink/tool/tool/google_calendar/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/dlink/tool/tool/google_calendar/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/home/dlink/tool/tool/google_calendar/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now = datetime.datetime.now().replace(
        minute=0, hour=0, second=0, microsecond=0, tzinfo=tw_tz).isoformat()
    end = datetime.datetime.now().replace(
        minute=59, hour=23, second=59, microsecond=0, tzinfo=tw_tz).isoformat()
    print(f'Getting the upcoming 10 events after [{now}] before [{end}]')
    #now = '2020-09-02T00:00:00+08:00'
    #end = '2020-09-02T23:59:59+08:00'
    events_result = service.events().list(
        calendarId='hsc6u56md5p0mjjn8jutt10ggc@group.calendar.google.com',
        timeMin=now,
        timeMax=end,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    usqa_intest = False
    if events:
        usqa_intest = True
    '''      
    for event in events:
        #print(json.dumps(event, indent=4))
        print(f'event:\nID[{event["id"]}]')
        if 'summary' in event:
            print(f'SUMMARY[{event["summary"]}]')
            if '[usqa]' in event['summary'].lower():
                usqa_intest = True
        if 'description' in event:
            print(f'TEXT[{event["description"]}]')

        print(f'START[{event["start"].get("date", event["start"].get("dateTime"))}]')
        print(f'END[{event["end"].get("date", event["end"].get("dateTime"))}]')
        print('\n\n')
        if usqa_intest:
            break
    '''

    r = redis.Redis(
        host=redis_url,
        port=redis_port,
        decode_responses=True
    )
    if usqa_intest:
        print('Set InTesting to True')
        r.set('in_testing', 'True')
    else:
        print('Set InTesting to False')
        r.set('in_testing', 'False')


if __name__ == '__main__':
    main()
