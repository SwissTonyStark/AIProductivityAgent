import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# The API scope required to interact with Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def generate_token():
    creds = None

    # The token file stores the user's access and refresh tokens and is created automatically
    # when the authorization flow completes for the first time.
    if os.path.exists('token_calendar.pickle'):
        with open('token_calendar.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_calendar_api.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token_calendar.pickle', 'wb') as token:
            pickle.dump(creds, token)

    print("Token for Google Calendar generated successfully!")

if __name__ == '__main__':
    generate_token()
