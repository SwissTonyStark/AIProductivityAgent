import os
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from utils.email_parser import parse_email
from utils.gmail_client import GmailClient
from utils.google_calendar_client import GoogleCalendarClient
from langchain.chains import LLMChain
from datetime import datetime

# --- Tavily Search Tool ---
@tool
def tavily_tool(query: str, max_results: int = 2):
    """
    Uses Tavily to perform a search and returns the results.
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY is missing from the environment variables.")
    # Initialize TavilySearchResults with the API key
    search_tool = TavilySearchResults(max_results=max_results, tavily_api_key=tavily_api_key)
    search_results = search_tool.search(query)  # Assuming the search method exists
    return search_results

# --- Email Parser Tool ---
@tool
def parse_email_tool(raw_email: str) -> dict:
    """
    Parses a raw email string and extracts metadata like from, to, subject, date, and body.
    Useful for understanding the content of incoming emails.
    """
    return parse_email(raw_email)

# --- Gmail: Get last N emails ---
@tool
def get_gmail_summary(n: int = 15) -> str:
    """
    Fetches the last N emails and returns a summary with sender and subject.
    """
    client = GmailClient()
    emails = client.get_recent_emails(max_results=n)
    return "\n\n".join([f"From: {e['from']}\nSubject: {e['subject']}\n" for e in emails])

# --- Gmail: Search by keyword ---
@tool
def search_gmail_by_keyword(keyword: str, n: int = 15) -> str:
    """
    Searches Gmail for emails containing the given keyword.
    Returns up to N matches with sender and subject.
    """
    client = GmailClient()
    emails = client.search_emails(keyword, max_results=n)
    if not emails:
        return f"No emails found containing '{keyword}'."
    return "\n\n".join([
        f"From: {e['from']}\nSubject: {e['subject']}\nSnippet: {e['snippet']}" for e in emails
    ])

# --- Google Calendar: Create Event ---
@tool
def create_google_event(summary: str, description: str, start_time: str, end_time: str) -> str:
    """
    Creates an event in Google Calendar using the provided parameters.
    """
    
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)

    client = GoogleCalendarClient()
    response = client.create_event(summary, description, start_dt, end_dt)
    return response

# --- List of tools for the agent ---
TOOLS = [
    tavily_tool,
    parse_email_tool,
    get_gmail_summary,
    search_gmail_by_keyword,
    create_google_event,  # Add the Google calendar event tool
]
