from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import pickle
import os.path

# google calendar api setup
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
creds = None

#  the file token.pickle stores the user's credentials and refresh tokens
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
# if there are no valid credentials, user logs in
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle','wb') as token:
        pickle.dump(creds,token)
        
service = build('calendar','v3',credentials=creds)

# define the events
'''
    This is a string in ISO 8601 format that specifies the start date and time of the event.
    "2023-07-01": The date part, indicating July 1, 2023.
    "T": The letter "T" is a delimiter that separates the date from the time.
    "09:00:00": The time part, indicating 9:00 AM.
    "-07:00": The time zone offset from UTC. Here, it indicates a time zone that is 7 hours behind UTC (e.g., Pacific Daylight Time).
    '''
events = [
    ("Introduction to Pandas: Series and DataFrames", "2024-06-26T03:00:00+03:00"),
]

# insert the events into the calendar
for event in events:
    event_body = {
        'summary':event[0],
        'start': {
            'dateTime':event[1],
            'timeZone': 'Africa/Nairobi',
        },
        'end': {
            'dateTime':(datetime.datetime.fromisoformat(event[1]) + datetime.timedelta(hours = 2)).isoformat(),
            'timeZone': 'Africa/Nairobi',
        }
    }
    service.events().insert(calendarId='primary', body = event_body).execute()