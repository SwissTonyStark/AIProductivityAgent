"""
Tools module providing various productivity-related functions for the agent.
Includes tools for web search, email management, and calendar operations.
"""
import os
from datetime import datetime
from typing import List, Optional, Dict, Any

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

# Available tools for the agent
TOOLS = [
    tavily_tool,
    parse_email_tool, 
    get_gmail_summary,
    search_gmail_by_keyword,
    create_google_event,
    get_upcoming_calendar_events
]
