import requests
import msal
import os
from dotenv import load_dotenv

load_dotenv()

class OutlookClient:
    def __init__(self):
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET")
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        self.access_token = self.authenticate()

    def authenticate(self):
        app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=self.authority,
        )
        result = app.acquire_token_for_client(scopes=self.scope)
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception("Authentication failed", result)

    def get_emails(self, folder="inbox", top=10):
        url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder}/messages?$top={top}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("value", [])
        else:
            raise Exception("Failed to fetch emails", response.text)
