import os
import json
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle

# Allow insecure transport for local development (localhost only)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRETS_FILE = 'credentials.json'
TOKEN_PICKLE_FILE = 'token.pickle'
DEMO_MODE = False  # Set to True only for demo testing

def get_google_flow():
    """Create and return a Google OAuth flow"""
    try:
        if not os.path.exists(CLIENT_SECRETS_FILE):
            raise FileNotFoundError(f"{CLIENT_SECRETS_FILE} not found. Please download credentials.json from Google Cloud Console.")
        
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri='http://localhost:8080/oauth2callback'
        )
        return flow
    except Exception as e:
        print(f"Error creating OAuth flow: {str(e)}")
        raise

def save_credentials(credentials):
    """Save credentials to pickle file"""
    with open(TOKEN_PICKLE_FILE, 'wb') as token:
        pickle.dump(credentials, token)

def load_credentials():
    """Load credentials from pickle file"""
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
            if creds and creds.valid:
                return creds
            elif creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                save_credentials(creds)
                return creds
    return None

def clear_credentials():
    """Clear saved credentials"""
    if os.path.exists(TOKEN_PICKLE_FILE):
        os.remove(TOKEN_PICKLE_FILE)
