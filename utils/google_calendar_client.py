"""
Google Calendar Client module that provides calendar operations through a unified class interface.
This module handles authentication and calendar operations for use with LangChain tools.
"""
import os
import pickle
from datetime import datetime
from typing import List, Optional, Dict, Any

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Scopes required for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarClient:
    """A client class for interacting with Google Calendar API."""
    
    def __init__(self):
        """Initialize the Google Calendar client with authenticated service."""
        self.service = self._authenticate()
    
    def _authenticate(self):
        """
        Handle Google Calendar authentication flow.
        
        Ensures fresh tokens are obtained when required by:
        1. Using existing valid credentials if available
        2. Refreshing expired credentials if possible
        3. Initiating a new auth flow if credentials are invalid or revoked
        """
        creds = None
        token_path = 'token_calendar.pickle'
        
        # Load existing token if available
        if os.path.exists(token_path):
            try:
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)
                print("Loaded existing credentials")
            except Exception as e:
                print(f"Error loading credentials: {e}")
                creds = None

        # Check if credentials need to be refreshed or recreated
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    print("Refreshing expired credentials")
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    # Force new token creation if refresh fails
                    creds = None
            
            # If credentials are still invalid, create new ones
            if not creds or not creds.valid:
                print("Obtaining new credentials")
                try:
                    # Try with credentials_calendar_api.json first
                    if os.path.exists('credentials_calendar_api.json'):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials_calendar_api.json', SCOPES)
                    # Fall back to credentials_gmail_api.json if calendar-specific file not found
                    elif os.path.exists('credentials_gmail_api.json'):
                        print("Using Gmail API credentials for Calendar authentication")
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials_gmail_api.json', SCOPES)
                    else:
                        raise FileNotFoundError("No credentials file found")
                    
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    raise RuntimeError(f"Failed to authenticate: {e}")

            # Save valid credentials for future use
            try:
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
                    print("Credentials saved successfully")
            except Exception as e:
                print(f"Warning: Could not save credentials: {e}")

        return build('calendar', 'v3', credentials=creds)

    def create_event(self, 
                    summary: str, 
                    description: str, 
                    start_time: datetime, 
                    end_time: datetime, 
                    attendees: Optional[List[str]] = None, 
                    reminders: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Create a new calendar event.
        
        Args:
            summary: Event title
            description: Event description
            start_time: Event start time
            end_time: Event end time
            attendees: List of attendee email addresses
            reminders: List of reminder settings
            
        Returns:
            str: URL of the created event
        """
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
        
        if reminders:
            event['reminders'] = {
                'useDefault': False,
                'overrides': reminders
            }
        else:
            event['reminders'] = {'useDefault': True}

        event_result = self.service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event_result.get('htmlLink')}"

    def get_upcoming_events(self, max_results: int = 10, time_min: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get upcoming calendar events.
        
        Args:
            max_results: Maximum number of events to return
            time_min: Start time for fetching events (defaults to current time)
            
        Returns:
            List of calendar events
        """
        if time_min is None:
            time_min = datetime.utcnow()
        
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=time_min.isoformat() + 'Z',
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])

    def create_reminder_settings(self, 
                               email_minutes: Optional[int] = 10, 
                               popup_minutes: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Create reminder settings for calendar events.
        
        Args:
            email_minutes: Minutes before event to send email reminder
            popup_minutes: Minutes before event to show popup reminder
            
        Returns:
            List of reminder settings
        """
        reminders = []
        
        if email_minutes is not None:
            reminders.append({'method': 'email', 'minutes': email_minutes})
        
        if popup_minutes is not None:
            reminders.append({'method': 'popup', 'minutes': popup_minutes})
        
        return reminders