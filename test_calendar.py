import os
from datetime import datetime
from utils.google_calendar_client import GoogleCalendarClient

# Define test details for event creation
event_details = {
    "summary": "Test Meeting",
    "description": "Discuss project milestones and next steps.",
    "start_time": datetime(2025, 4, 1, 15, 0),  # Set to a valid datetime
    "end_time": datetime(2025, 4, 1, 16, 0),    # Set to a valid datetime
    "attendees": ["email@example.com", "anotheremail@example.com"],  # Replace with valid email addresses
}

def test_create_event():
    try:
        print("Testing Google Calendar Event Creation...")

        # Initialize the GoogleCalendarClient
        calendar_client = GoogleCalendarClient()
        
        # Call the create_event method with attendees
        event_link = calendar_client.create_event(
            summary=event_details["summary"],
            description=event_details["description"],
            start_time=event_details["start_time"],
            end_time=event_details["end_time"],
            attendees=event_details["attendees"]  # Pass the list of attendees as a keyword argument
        )

        # Print success message with the event link
        print(f"Event '{event_details['summary']}' created successfully!")
        print(f"Event details: {event_link}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_create_event()
