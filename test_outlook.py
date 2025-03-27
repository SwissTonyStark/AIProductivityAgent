"""
    The script is currently working, but I need IT permissions to access 
    the Outlook API. I will test it later.
"""

import os
from msal import PublicClientApplication
import requests
from dotenv import load_dotenv

load_dotenv()

class OutlookClient:
    def __init__(self):
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.scopes = ["Mail.Read"]
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.token = self.authenticate()

    def authenticate(self):
        app = PublicClientApplication(client_id=self.client_id, authority=self.authority)
        flow = app.initiate_device_flow(scopes=self.scopes)

        if "user_code" not in flow:
            raise Exception("❌ Could not create device flow")

        print(f"🔑 Please authenticate: {flow['message']}")
        result = app.acquire_token_by_device_flow(flow)

        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception("❌ Authentication failed", result)

    def get_recent_emails(self, user_id="me", count=5):
        url = f"https://graph.microsoft.com/v1.0/{user_id}/messages?$top={count}&$orderby=receivedDateTime desc"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            messages = response.json().get("value", [])
            return [
                {
                    "subject": m.get("subject"),
                    "from": m.get("from", {}).get("emailAddress", {}).get("address"),
                    "body_preview": m.get("bodyPreview")
                }
                for m in messages
            ]
        else:
            raise Exception("Failed to fetch emails", response.text)

if __name__ == "__main__":
    try:
        client = OutlookClient()
        emails = client.get_recent_emails()
        print("\n📥 Recent Emails:")
        for i, email in enumerate(emails, 1):
            print(f"\nEmail #{i}")
            print(f"From: {email['from']}")
            print(f"Subject: {email['subject']}")
            print(f"Preview: {email['body_preview']}")
    except Exception as e:
        print("❌ Error:", e)
