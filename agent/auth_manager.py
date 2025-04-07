"""
Authentication manager that handles all authentication flows for the productivity agent.
This includes Azure OpenAI, Gmail, and Google Calendar authentication.
"""
import os
import pickle
from typing import Dict, Any, Optional
import streamlit as st
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

load_dotenv()

class AuthManager:
    def __init__(self):
        """Initialize the authentication manager."""
        self.gmail_creds = None
        self.calendar_creds = None
        self.azure_openai_config = {
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
            "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        }

    def authenticate_all(self) -> bool:
        """Authenticate all services and return True if all successful."""
        try:
            self._authenticate_gmail()
            self._authenticate_calendar()
            return True
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            return False

    def _authenticate_gmail(self):
        """Handle Gmail authentication."""
        SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
        token_path = "token_gmail.pickle"
        
        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                self.gmail_creds = pickle.load(token)
        
        if not self.gmail_creds or not self.gmail_creds.valid:
            if self.gmail_creds and self.gmail_creds.expired and self.gmail_creds.refresh_token:
                self.gmail_creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials_gmail_api.json', SCOPES)
                self.gmail_creds = flow.run_local_server(port=0)
            
            with open(token_path, 'wb') as token:
                pickle.dump(self.gmail_creds, token)

    def _authenticate_calendar(self):
        """Handle Google Calendar authentication."""
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        token_path = 'token_calendar.pickle'
        
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.calendar_creds = pickle.load(token)
        
        if not self.calendar_creds or not self.calendar_creds.valid:
            if self.calendar_creds and self.calendar_creds.expired and self.calendar_creds.refresh_token:
                self.calendar_creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials_calendar_api.json', SCOPES)
                self.calendar_creds = flow.run_local_server(port=0)
            
            with open(token_path, 'wb') as token:
                pickle.dump(self.calendar_creds, token)

    def get_gmail_service(self):
        """Get authenticated Gmail service."""
        if not self.gmail_creds:
            self._authenticate_gmail()
        return build("gmail", "v1", credentials=self.gmail_creds)

    def get_calendar_service(self):
        """Get authenticated Google Calendar service."""
        if not self.calendar_creds:
            self._authenticate_calendar()
        return build('calendar', 'v3', credentials=self.calendar_creds)

    def get_azure_openai_config(self):
        """Get Azure OpenAI configuration."""
        return self.azure_openai_config 