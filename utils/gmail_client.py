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
        token_path = "token_gmail.pickle"
        
        # Load existing token if available
        if os.path.exists(token_path):
            try:
                with open(token_path, "rb") as token:
                    self.creds = pickle.load(token)
                print("Loaded existing Gmail credentials")
            except Exception as e:
                print(f"Error loading Gmail credentials: {e}")
                self.creds = None

        # Check if credentials need to be refreshed or recreated
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    print("Refreshing expired Gmail credentials")
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing Gmail credentials: {e}")
                    # Force new token creation if refresh fails
                    self.creds = None
            
            # If credentials are still invalid, create new ones
            if not self.creds or not self.creds.valid:
                print("Obtaining new Gmail credentials")
                try:
                    # Try with credentials_gmail_api.json
                    if os.path.exists('credentials_gmail_api.json'):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials_gmail_api.json', SCOPES)
                    elif os.path.exists('credentials.json'):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', SCOPES)
                    else:
                        raise FileNotFoundError("No Gmail credentials file found")
                    
                    self.creds = flow.run_local_server(port=0)
                except Exception as e:
                    raise RuntimeError(f"Failed to authenticate with Gmail: {e}")

            # Save valid credentials for future use
            try:
                with open(token_path, 'wb') as token:
                    pickle.dump(self.creds, token)
                    print("Gmail credentials saved successfully")
            except Exception as e:
                print(f"Warning: Could not save Gmail credentials: {e}")

        self.service = build("gmail", "v1", credentials=self.creds)

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
