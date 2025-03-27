from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from utils.email_parser import parse_email
from utils.gmail_client import GmailClient

# --- Tavily Search Tool ---
tavily_tool = TavilySearchResults(max_results=2)

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
def get_gmail_summary(n: int = 5) -> str:
    """
    Fetches the last N emails and returns a summary with sender and subject.
    """
    client = GmailClient()
    emails = client.get_recent_emails(max_results=n)
    return "\n\n".join([f"From: {e['from']}\nSubject: {e['subject']}\n" for e in emails])

# --- Gmail: Search by keyword ---
@tool
def search_gmail_by_keyword(keyword: str, n: int = 5) -> str:
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

# --- List of tools for the agent ---
TOOLS = [
    tavily_tool,
    parse_email_tool,
    get_gmail_summary,
    search_gmail_by_keyword,
]