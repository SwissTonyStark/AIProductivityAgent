"""
Google Calendar Client module that provides calendar operations through a unified class interface.
This module uses the AuthManager for authentication and calendar operations.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from googleapiclient.discovery import build
from agent.auth_manager import AuthManager

class GoogleCalendarClient:
    """A client class for interacting with Google Calendar API."""
    
    def __init__(self, auth_manager: AuthManager):
        """Initialize the Google Calendar client with an AuthManager instance."""
        self.auth_manager = auth_manager
        self.service = self.auth_manager.get_calendar_service()

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