"""
    This module provides Gmail integration for our LangChain productivity agent.
    It uses the AuthManager for authentication and the Gmail API to fetch messages.
    Make sure to enable the Gmail API for your Google Cloud project and generate
    OAuth 2.0 credentials with the correct scopes.
"""

from typing import List, Dict, Any, Optional
from googleapiclient.discovery import build
from agent.auth_manager import AuthManager
import base64
from email.mime.text import MIMEText
from datetime import datetime

# Updated scopes to include modify and send capabilities
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send"
]

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
        return self._process_messages(messages)

    def search_emails(self, query: str, max_results: int = 15) -> List[dict]:
        """Searches emails matching the query and returns basic metadata."""
        results = self.service.users().messages().list(
            userId='me', 
            q=query, 
            maxResults=max_results
        ).execute()
        messages = results.get('messages', [])
        return self._process_messages(messages)

    def _process_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Helper method to process message data consistently."""
        emails = []
        for msg in messages:
            try:
                msg_data = self.service.users().messages().get(
                    userId='me', 
                    id=msg['id']
                ).execute()
                
                payload = msg_data.get('payload', {})
                headers = payload.get('headers', [])
                
                email_data = {
                    'id': msg['id'],
                    'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)'),
                    'from': next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)'),
                    'date': next((h['value'] for h in headers if h['name'] == 'Date'), ''),
                    'snippet': msg_data.get('snippet', ''),
                    'labels': msg_data.get('labelIds', [])
                }
                
                # Extract email body
                if 'parts' in payload:
                    parts = payload['parts']
                    data = parts[0]['body'].get('data', '')
                else:
                    data = payload['body'].get('data', '')
                
                if data:
                    text = base64.urlsafe_b64decode(data).decode()
                    email_data['body'] = text
                
                emails.append(email_data)
            except Exception as e:
                continue
        
        return emails

    def batch_modify_labels(
        self, 
        message_ids: List[str], 
        add_labels: Optional[List[str]] = None,
        remove_labels: Optional[List[str]] = None
    ) -> bool:
        """
        Modifies labels for multiple messages in batch.
        
        Args:
            message_ids: List of message IDs to modify
            add_labels: Labels to add
            remove_labels: Labels to remove
            
        Returns:
            bool: Success status
        """
        try:
            body = {
                'ids': message_ids,
                'addLabelIds': add_labels or [],
                'removeLabelIds': remove_labels or []
            }
            
            self.service.users().messages().batchModify(
                userId='me',
                body=body
            ).execute()
            return True
        except Exception as e:
            return False

    def archive_messages(self, message_ids: List[str]) -> bool:
        """
        Archives multiple messages by removing INBOX label.
        
        Args:
            message_ids: List of message IDs to archive
            
        Returns:
            bool: Success status
        """
        return self.batch_modify_labels(
            message_ids=message_ids,
            remove_labels=['INBOX']
        )

    def mark_as_read(self, message_ids: List[str]) -> bool:
        """
        Marks multiple messages as read by removing UNREAD label.
        
        Args:
            message_ids: List of message IDs to mark as read
            
        Returns:
            bool: Success status
        """
        return self.batch_modify_labels(
            message_ids=message_ids,
            remove_labels=['UNREAD']
        )

    def send_email(
        self, 
        to: str, 
        subject: str, 
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Sends an email using the Gmail API.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients
            
        Returns:
            bool: Success status
        """
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = ', '.join(cc)
            if bcc:
                message['bcc'] = ', '.join(bcc)
                
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('utf-8')
            
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return True
        except Exception as e:
            return False
