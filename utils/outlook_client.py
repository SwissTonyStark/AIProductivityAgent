"""
Outlook client module - Currently not in use
"""
# import requests
# from agent.auth_manager import AuthManager

# class OutlookClient:
#     def __init__(self, auth_manager: AuthManager):
#         """Initialize the Outlook client with an AuthManager instance."""
#         self.auth_manager = auth_manager
#         self.access_token = self.auth_manager.get_outlook_token()

#     def get_emails(self, folder="inbox", top=10):
#         url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder}/messages?$top={top}"
#         headers = {"Authorization": f"Bearer {self.access_token}"}
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             return response.json().get("value", [])
#         else:
#             raise Exception("Failed to fetch emails", response.text)
