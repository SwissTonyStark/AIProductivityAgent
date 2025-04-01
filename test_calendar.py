import os
from datetime import datetime
from utils.google_calendar_client import create_google_event

# Define test details for event creation
event_details = {
    "summary": "Test Meeting",
    "description": "Discuss project milestones and next steps.",
    "start_time": "2025-04-01T15:00:00",  # Set to a valid datetime
    "end_time": "2025-04-01T16:00:00",    # Set to a valid datetime
    "attendees": ["email@example.com"],    # Replace with valid email addresses
}

def test_create_event():
    try:
        print("Testing Google Calendar Event Creation...")
        # Call the create_google_event function
        create_google_event(
            event_details["summary"],
            event_details["description"],
            event_details["start_time"],
            event_details["end_time"],
            event_details["attendees"]
        )
        print(f"Event '{event_details['summary']}' created successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_create_event()
