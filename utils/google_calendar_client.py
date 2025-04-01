import os
import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Authenticate and create Google Calendar client
def get_google_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds, _ = google.auth.load_credentials_from_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_calendar_api.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

# Function to create an event in Google Calendar
def create_google_event(summary, description, start_time, end_time):
    service = get_google_calendar_service()
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return f"Event created: {event_result.get('htmlLink')}"
