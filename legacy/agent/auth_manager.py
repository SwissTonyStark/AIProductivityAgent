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
from functools import lru_cache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class AuthManager:
    def __init__(self):
        """Initialize the authentication manager."""
        self.gmail_creds = None
        self.calendar_creds = None
        self._validate_env_vars()
        self.azure_openai_config = {
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
            "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        }

    def _validate_env_vars(self):
        """Validate required environment variables."""
        required_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_VERSION",
            "AZURE_OPENAI_DEPLOYMENT_NAME"
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    def authenticate_all(self) -> bool:
        """Authenticate all services and return True if all successful."""
        try:
            self._authenticate_gmail()
            self._authenticate_calendar()
            return True
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            st.error(f"Authentication failed: {str(e)}")
            return False

    def _authenticate_service(self, scopes: list, token_path: str, credentials_file: str) -> Credentials:
        """Generic authentication method for Google services."""
        creds = None
        
        try:
            if os.path.exists(token_path):
                with open(token_path, "rb") as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
                    creds = flow.run_local_server(port=0)
                
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
            
            return creds
        except Exception as e:
            logger.error(f"Authentication error for {token_path}: {str(e)}")
            raise

    def _authenticate_gmail(self):
        """Handle Gmail authentication."""
        SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
        self.gmail_creds = self._authenticate_service(
            SCOPES, 
            "token_gmail.pickle", 
            'credentials_gmail_api.json'
        )

    def _authenticate_calendar(self):
        """Handle Google Calendar authentication."""
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.calendar_creds = self._authenticate_service(
            SCOPES, 
            'token_calendar.pickle', 
            'credentials_calendar_api.json'
        )

    @lru_cache(maxsize=1)
    def get_gmail_service(self):
        """Get authenticated Gmail service with caching."""
        if not self.gmail_creds:
            self._authenticate_gmail()
        return build("gmail", "v1", credentials=self.gmail_creds)

    @lru_cache(maxsize=1)
    def get_calendar_service(self):
        """Get authenticated Google Calendar service with caching."""
        if not self.calendar_creds:
            self._authenticate_calendar()
        return build('calendar', 'v3', credentials=self.calendar_creds)

    def get_azure_openai_config(self) -> Dict[str, str]:
        """Get Azure OpenAI configuration."""
        return self.azure_openai_config.copy()  # Return a copy to prevent modification 