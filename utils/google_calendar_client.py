#google_calendar_client.py
import os
import google.auth
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime

# Scopes for Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Authenticate and create Google Calendar client
def get_google_calendar_service():
    creds = None
    # Check if we already have the token for calendar
    if os.path.exists('token_calendar.pickle'):
        # Load the calendar credentials from the token file
        with open('token_calendar.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there's no valid creds, or if they're expired, prompt for authorization
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_calendar_api.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the new credentials for future use
        with open('token_calendar.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

# Function to create an event in Google Calendar, including attendees
def create_google_event(summary, description, start_time, end_time, attendees=None):
    service = get_google_calendar_service()

    # Build event details
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

    if attendees:
        event['attendees'] = [{'email': attendee} for attendee in attendees]

    # Insert the event into Google Calendar
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return f"Event created: {event_result.get('htmlLink')}"
