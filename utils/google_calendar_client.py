"""
Google Calendar Client module that provides calendar operations through a unified class interface.
This module uses the AuthManager for authentication and calendar operations.
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from collections import Counter
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
                    reminders: Optional[List[Dict[str, Any]]] = None,
                    location: Optional[str] = None,
                    conference_solution: Optional[str] = None) -> str:
        """
        Create a new calendar event with enhanced options.
        
        Args:
            summary: Event title
            description: Event description
            start_time: Event start time
            end_time: Event end time
            attendees: List of attendee email addresses
            reminders: List of reminder settings
            location: Optional physical location
            conference_solution: Optional video conference type ('meet' or 'zoom')
            
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

        if location:
            event['location'] = location

        if attendees:
            event['attendees'] = [{'email': attendee} for attendee in attendees]
        
        if reminders:
            event['reminders'] = {
                'useDefault': False,
                'overrides': reminders
            }
        else:
            event['reminders'] = {'useDefault': True}

        if conference_solution:
            if conference_solution.lower() == 'meet':
                event['conferenceData'] = {
                    'createRequest': {
                        'requestId': f"{summary}-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                    }
                }

        event_result = self.service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1 if conference_solution else 0
        ).execute()
        
        return f"Event created: {event_result.get('htmlLink')}"

    def get_upcoming_events(self, 
                          max_results: int = 10, 
                          time_min: Optional[datetime] = None,
                          calendar_id: str = 'primary') -> List[Dict[str, Any]]:
        """
        Get upcoming calendar events with enhanced filtering.
        
        Args:
            max_results: Maximum number of events to return
            time_min: Start time for fetching events (defaults to current time)
            calendar_id: Calendar ID to fetch events from
            
        Returns:
            List of calendar events
        """
        if time_min is None:
            time_min = datetime.utcnow()
        
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=time_min.isoformat() + 'Z',
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])

    def find_available_slots(self,
                           participants: List[str],
                           duration_minutes: int,
                           start_date: datetime,
                           end_date: datetime,
                           working_hours: Optional[Dict[str, Tuple[int, int]]] = None) -> List[datetime]:
        """
        Find available time slots for all participants.
        
        Args:
            participants: List of participant email addresses
            duration_minutes: Desired meeting duration
            start_date: Start of search range
            end_date: End of search range
            working_hours: Optional dict mapping weekdays to (start_hour, end_hour)
            
        Returns:
            List of available datetime slots
        """
        if not working_hours:
            working_hours = {
                'Monday': (9, 17),
                'Tuesday': (9, 17),
                'Wednesday': (9, 17),
                'Thursday': (9, 17),
                'Friday': (9, 17)
            }
        
        # Get busy periods for all participants
        busy_periods = []
        for participant in participants:
            free_busy_query = {
                'timeMin': start_date.isoformat(),
                'timeMax': end_date.isoformat(),
                'items': [{'id': participant}]
            }
            
            result = self.service.freebusy().query(body=free_busy_query).execute()
            calendars = result.get('calendars', {})
            
            for calendar_id, calendar_data in calendars.items():
                busy_periods.extend(calendar_data.get('busy', []))
        
        # Find available slots
        available_slots = []
        current_time = start_date
        
        while current_time < end_date:
            weekday = current_time.strftime('%A')
            if weekday in working_hours:
                start_hour, end_hour = working_hours[weekday]
                
                # Check if current time is within working hours
                if start_hour <= current_time.hour < end_hour:
                    slot_end = current_time + timedelta(minutes=duration_minutes)
                    
                    # Check if slot conflicts with any busy period
                    is_available = True
                    for busy in busy_periods:
                        busy_start = datetime.fromisoformat(busy['start'].rstrip('Z'))
                        busy_end = datetime.fromisoformat(busy['end'].rstrip('Z'))
                        
                        if (current_time < busy_end and slot_end > busy_start):
                            is_available = False
                            break
                    
                    if is_available:
                        available_slots.append(current_time)
            
            current_time += timedelta(minutes=30)
        
        return available_slots

    def analyze_meeting_patterns(self, 
                               start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Analyze calendar patterns to provide insights.
        
        Args:
            start_date: Optional start date for analysis
            end_date: Optional end date for analysis
            
        Returns:
            Dict containing calendar analytics
        """
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
            
        events = self.get_upcoming_events(
            max_results=1000,
            time_min=start_date
        )
        
        # Initialize analysis
        analysis = {
            'total_meetings': len(events),
            'total_duration': timedelta(),
            'meetings_by_day': Counter(),
            'meetings_by_hour': Counter(),
            'common_participants': Counter(),
            'recurring_meetings': 0,
            'meeting_categories': Counter(),
            'avg_meeting_duration': timedelta(),
            'suggestions': []
        }
        
        for event in events:
            # Get start and end times
            start = event.get('start', {}).get('dateTime')
            end = event.get('end', {}).get('dateTime')
            
            if start and end:
                start_dt = datetime.fromisoformat(start.rstrip('Z'))
                end_dt = datetime.fromisoformat(end.rstrip('Z'))
                duration = end_dt - start_dt
                
                # Update analysis
                analysis['total_duration'] += duration
                analysis['meetings_by_day'][start_dt.strftime('%A')] += 1
                analysis['meetings_by_hour'][start_dt.hour] += 1
                
                # Track participants
                for attendee in event.get('attendees', []):
                    analysis['common_participants'][attendee.get('email')] += 1
                    
                # Check if recurring
                if 'recurringEventId' in event:
                    analysis['recurring_meetings'] += 1
                    
                # Categorize meeting
                summary = event.get('summary', '').lower()
                if 'standup' in summary:
                    analysis['meeting_categories']['standup'] += 1
                elif 'review' in summary:
                    analysis['meeting_categories']['review'] += 1
                elif 'planning' in summary:
                    analysis['meeting_categories']['planning'] += 1
                else:
                    analysis['meeting_categories']['other'] += 1
        
        # Calculate averages and generate suggestions
        if analysis['total_meetings'] > 0:
            analysis['avg_meeting_duration'] = analysis['total_duration'] / analysis['total_meetings']
            
            # Generate insights
            busy_days = [day for day, count in analysis['meetings_by_day'].items() if count > 3]
            if busy_days:
                analysis['suggestions'].append(
                    f"Consider reducing meetings on {', '.join(busy_days)}"
                )
            
            if analysis['avg_meeting_duration'] > timedelta(hours=1):
                analysis['suggestions'].append(
                    "Consider shorter meeting durations for better productivity"
                )
                
            if analysis['recurring_meetings'] / analysis['total_meetings'] > 0.5:
                analysis['suggestions'].append(
                    "High number of recurring meetings - review their necessity"
                )
        
        return analysis

    def create_reminder_settings(self, 
                               email_minutes: Optional[int] = 10, 
                               popup_minutes: Optional[int] = None,
                               sms_minutes: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Create reminder settings for calendar events.
        
        Args:
            email_minutes: Minutes before event to send email reminder
            popup_minutes: Minutes before event to show popup reminder
            sms_minutes: Minutes before event to send SMS reminder
            
        Returns:
            List of reminder settings
        """
        reminders = []
        
        if email_minutes is not None:
            reminders.append({'method': 'email', 'minutes': email_minutes})
        
        if popup_minutes is not None:
            reminders.append({'method': 'popup', 'minutes': popup_minutes})
            
        if sms_minutes is not None:
            reminders.append({'method': 'sms', 'minutes': sms_minutes})
        
        return reminders