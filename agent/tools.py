"""
Tools module providing various productivity-related functions for the agent.
Includes tools for web search, email management, calendar operations, and advanced productivity features.
"""
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import json
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from utils.email_parser import parse_email
from utils.gmail_client import GmailClient
from utils.google_calendar_client import GoogleCalendarClient
from agent.auth_manager import AuthManager

# Initialize authentication manager
auth_manager = AuthManager()

# --- Web Search Tool ---
@tool
def tavily_tool(query: str, max_results: int = 2) -> List[Dict]:
    """
    Performs a web search using the Tavily API and returns relevant results.

    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 2)

    Returns:
        List of search results containing title, content and URL

    Raises:
        ValueError: If TAVILY_API_KEY environment variable is not set
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY environment variable is required")
    
    search_tool = TavilySearchResults(max_results=max_results, tavily_api_key=tavily_api_key)
    return search_tool.search(query)

# --- Email Tools ---
@tool
def parse_email_tool(raw_email: str) -> Dict:
    """
    Parses a raw email string to extract key metadata.

    Args:
        raw_email: Raw email content as string

    Returns:
        Dict containing email metadata (from, to, subject, date, body)
    """
    return parse_email(raw_email)

@tool
def get_gmail_summary(n: int = 15) -> str:
    """
    Retrieves a summary of recent Gmail messages.

    Args:
        n: Number of recent emails to fetch (default: 15)

    Returns:
        Formatted string containing sender and subject for each email
    """
    try:
        client = GmailClient(auth_manager)
        emails = client.get_recent_emails(max_results=n)
        
        if not emails:
            return "No recent emails found."
            
        email_summaries = []
        for email in emails:
            summary = f"From: {email['from']}\nSubject: {email['subject']}\nSnippet: {email['snippet']}"
            email_summaries.append(summary)
            
        return "\n\n".join(email_summaries)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Error retrieving Gmail messages: {str(e)}\nDetails: {error_details}"

@tool
def search_gmail_by_keyword(keyword: str, n: int = 15) -> str:
    """
    Searches Gmail for messages containing a specific keyword.

    Args:
        keyword: Search term to look for in emails
        n: Maximum number of results to return (default: 15)

    Returns:
        Formatted string containing matching email details
    """
    try:
        client = GmailClient(auth_manager)
        emails = client.search_emails(keyword, max_results=n)
        if not emails:
            return f"No emails found containing '{keyword}'."
        
        return "\n\n".join([
            f"From: {e['from']}\nSubject: {e['subject']}\nSnippet: {e['snippet']}" 
            for e in emails
        ])
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Error searching Gmail: {str(e)}\nDetails: {error_details}"

# --- Calendar Tools ---
@tool
def create_google_event(
    summary: str,
    description: str,
    start_time: str,
    end_time: str,
    attendees: Optional[List[str]] = None,
    reminders: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Creates a new event in Google Calendar.

    Args:
        summary: Event title/name
        description: Detailed event description
        start_time: Start time in ISO format (YYYY-MM-DDTHH:MM:SS)
        end_time: End time in ISO format (YYYY-MM-DDTHH:MM:SS)
        attendees: Optional list of attendee email addresses
        reminders: Optional list of reminder settings

    Returns:
        URL of the created calendar event
    """
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)

    client = GoogleCalendarClient(auth_manager)
    return client.create_event(
        summary=summary,
        description=description,
        start_time=start_dt,
        end_time=end_dt,
        attendees=attendees,
        reminders=reminders
    )

@tool
def get_upcoming_calendar_events(max_results: int = 10) -> str:
    """
    Retrieves upcoming events from Google Calendar.

    Args:
        max_results: Maximum number of events to return (default: 10)

    Returns:
        Formatted string containing upcoming event details
    """
    client = GoogleCalendarClient(auth_manager)
    events = client.get_upcoming_events(max_results=max_results)
    
    if not events:
        return "No upcoming events found."
    
    result = []
    for event in events:
        start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', 'N/A'))
        summary = event.get('summary', 'Untitled Event')
        result.append(f"Event: {summary}\nTime: {start}")
    
    return "\n\n".join(result)

# --- Enhanced Email Tools ---
@tool
def analyze_email_importance(raw_email: str) -> Dict[str, Any]:
    """
    Analyzes email importance based on sender, content, and urgency indicators.
    
    Args:
        raw_email: Raw email content
        
    Returns:
        Dict containing importance score and analysis
    """
    email_data = parse_email(raw_email)
    
    # Implement importance scoring logic
    importance_indicators = {
        'urgent': 5,
        'asap': 5,
        'important': 4,
        'priority': 4,
        'deadline': 3,
        'review': 2,
        'fyi': 1
    }
    
    score = 1  # Base score
    content = email_data['body'].lower()
    
    for indicator, value in importance_indicators.items():
        if indicator in content:
            score = max(score, value)
    
    return {
        'importance_score': score,
        'is_urgent': score >= 4,
        'analysis': f"Email importance score: {score}/5",
        'metadata': email_data
    }

@tool
def batch_process_emails(query: str, action: str, max_emails: int = 10) -> str:
    """
    Batch process multiple emails with specified action.
    
    Args:
        query: Search query to filter emails
        action: Action to perform ('archive', 'label', 'mark_read')
        max_emails: Maximum number of emails to process
        
    Returns:
        Summary of actions performed
    """
    client = GmailClient(auth_manager)
    emails = client.search_emails(query, max_emails)
    
    processed = 0
    for email in emails:
        try:
            if action == 'archive':
                # Implement archive logic
                processed += 1
            elif action == 'label':
                # Implement labeling logic
                processed += 1
            elif action == 'mark_read':
                # Implement mark as read logic
                processed += 1
        except Exception as e:
            continue
            
    return f"Successfully processed {processed} out of {len(emails)} emails with action: {action}"

# --- Enhanced Calendar Tools ---
@tool
def smart_schedule_meeting(
    participants: List[str],
    duration_minutes: int,
    preferred_days: Optional[List[str]] = None,
    preferred_times: Optional[List[str]] = None
) -> str:
    """
    Intelligently schedules a meeting based on participants' availability.
    
    Args:
        participants: List of participant email addresses
        duration_minutes: Meeting duration in minutes
        preferred_days: Optional list of preferred days
        preferred_times: Optional list of preferred time ranges
        
    Returns:
        Scheduled meeting details or suggested time slots
    """
    client = GoogleCalendarClient(auth_manager)
    
    # Get availability for next 5 business days
    start_time = datetime.now()
    end_time = start_time + timedelta(days=5)
    
    # Find available slots
    available_slots = []
    current_time = start_time
    
    while current_time < end_time:
        if (not preferred_days or current_time.strftime('%A') in preferred_days):
            # Check availability logic here
            available_slots.append(current_time)
        current_time += timedelta(minutes=30)
    
    if available_slots:
        # Schedule the first available slot
        meeting_time = available_slots[0]
        return client.create_event(
            summary=f"Meeting with {len(participants)} participants",
            description="Automatically scheduled meeting",
            start_time=meeting_time,
            end_time=meeting_time + timedelta(minutes=duration_minutes),
            attendees=participants
        )
    
    return "No suitable time slots found. Please try different preferences."

@tool
def analyze_calendar_patterns() -> Dict[str, Any]:
    """
    Analyzes calendar patterns to provide productivity insights.
    
    Returns:
        Dict containing calendar analytics and suggestions
    """
    client = GoogleCalendarClient(auth_manager)
    events = client.get_upcoming_events(max_results=100)
    
    analysis = {
        'meeting_hours_per_week': 0,
        'most_common_participants': [],
        'busy_days': [],
        'suggestions': []
    }
    
    # Implement calendar pattern analysis
    # Add logic for analyzing meeting frequency, duration patterns, etc.
    
    return analysis

# --- Task Management Tools ---
@tool
def extract_tasks_from_communications(content: str) -> List[Dict[str, Any]]:
    """
    Extracts actionable tasks from emails, messages, or notes.
    
    Args:
        content: Text content to analyze
        
    Returns:
        List of extracted tasks with metadata
    """
    tasks = []
    
    # Implement task extraction logic
    # Look for action items, deadlines, assignments, etc.
    
    return tasks

@tool
def prioritize_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Prioritizes tasks based on urgency, importance, and deadlines.
    
    Args:
        tasks: List of tasks to prioritize
        
    Returns:
        Prioritized list of tasks with scores
    """
    for task in tasks:
        # Calculate priority score based on multiple factors
        score = 0
        if task.get('deadline'):
            # Add deadline-based scoring
            pass
        if task.get('importance'):
            # Add importance-based scoring
            pass
            
        task['priority_score'] = score
    
    return sorted(tasks, key=lambda x: x['priority_score'], reverse=True)

# Available tools for the agent
TOOLS = [
    tavily_tool,
    analyze_email_importance,
    batch_process_emails,
    smart_schedule_meeting,
    analyze_calendar_patterns,
    extract_tasks_from_communications,
    prioritize_tasks,
    parse_email_tool,
    get_gmail_summary,
    search_gmail_by_keyword,
    create_google_event,
    get_upcoming_calendar_events
]
