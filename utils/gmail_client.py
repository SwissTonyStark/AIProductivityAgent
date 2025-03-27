"""
    This module provides Gmail integration for our LangChain productivity agent.
    It uses OAuth2 to authenticate and the Gmail API to fetch messages.
    Make sure to enable the Gmail API for your Google Cloud project and generate
    OAuth 2.0 credentials with the correct scopes.
"""

import os
import pickle
from typing import List
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the token.pickle file
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailClient:
    def __init__(self):
        """Initializes the Gmail client and authorizes using OAuth2."""
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Handles OAuth2 flow and creates the Gmail API service."""
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.creds = pickle.load(token)

        # If there are no (valid) credentials available, start the OAuth2 flow
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open("token.pickle", "wb") as token:
                pickle.dump(self.creds, token)

        self.service = build("gmail", "v1", credentials=self.creds)

    def get_recent_emails(self, max_results: int = 5) -> List[dict]:
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
    
    def search_emails(self, query: str, max_results: int = 5) -> List[dict]:
        results = self.service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])

        emails = []
        for msg in messages:
            msg_data = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
            snippet = msg_data.get('snippet', '')
            emails.append({'subject': subject, 'from': sender, 'snippet': snippet})
        
        return emails

