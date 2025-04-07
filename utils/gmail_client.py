"""
    This module provides Gmail integration for our LangChain productivity agent.
    It uses the AuthManager for authentication and the Gmail API to fetch messages.
    Make sure to enable the Gmail API for your Google Cloud project and generate
    OAuth 2.0 credentials with the correct scopes.
"""

from typing import List
from googleapiclient.discovery import build
from agent.auth_manager import AuthManager

# If modifying these scopes, delete the token_gmail.pickle file
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailClient:
    def __init__(self, auth_manager: AuthManager):
        """Initializes the Gmail client with an AuthManager instance."""
        self.auth_manager = auth_manager
        self.service = self.auth_manager.get_gmail_service()

    def get_recent_emails(self, max_results: int = 15) -> List[dict]:
        """Fetches recent emails with basic metadata (subject, sender, snippet)."""
        results = (
            self.service.users()
            .messages()
            .list(userId="me", maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            msg_data = (
                self.service.users()
                .messages()
                .get(userId="me", id=msg["id"])
                .execute()
            )
            headers = msg_data["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)")
            snippet = msg_data.get("snippet", "")

            emails.append({
                "subject": subject,
                "from": sender,
                "snippet": snippet
            })

        return emails
    
    def search_emails(self, query: str, max_results: int = 15) -> List[dict]:
        """Searches emails matching the query and returns basic metadata."""
        results = self.service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])

        emails = []
        for msg in messages:
            msg_data = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
            snippet = msg_data.get('snippet', '')
            emails.append({'subject': subject, 'from': sender, 'snippet': snippet})
        
        return emails
