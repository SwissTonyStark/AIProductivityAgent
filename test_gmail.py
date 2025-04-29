# test_gmail.py

from utils.gmail_client import GmailClient
from agent.auth_manager import AuthManager

auth_manager = AuthManager()
client = GmailClient(auth_manager)
emails = client.get_recent_emails()

print("\n📥 Gmail Inbox:")
for i, email in enumerate(emails, 1):
    print(f"\nEmail #{i}")
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Snippet: {email['snippet']}")
