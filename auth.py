import os
import json
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle

# Detect if running on Railway (check for Railway-specific variables)
IS_RAILWAY = bool(os.environ.get('RAILWAY_PUBLIC_DOMAIN') or os.environ.get('RAILWAY_ENVIRONMENT'))

# Allow insecure transport ONLY for local development (not on Railway)
if not IS_RAILWAY:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRETS_FILE = 'credentials.json'
TOKEN_PICKLE_FILE = 'token.pickle'
DEMO_MODE = False  # Set to True only for demo testing

def get_google_flow():
    """Create and return a Google OAuth flow"""
    try:
        creds_data = None
        
        # Try to load from environment variable first (for Railway/Production)
        env_creds = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        if env_creds:
            print("[AUTH] Loading credentials from environment variable GOOGLE_CREDENTIALS_JSON")
            creds_data = json.loads(env_creds)
        # Fall back to file (for local development)
        elif os.path.exists(CLIENT_SECRETS_FILE):
            print(f"[AUTH] Loading credentials from {CLIENT_SECRETS_FILE}")
            with open(CLIENT_SECRETS_FILE, 'r') as f:
                creds_data = json.load(f)
        else:
            raise FileNotFoundError(
                f"{CLIENT_SECRETS_FILE} not found.\n"
                "For local development: Download credentials.json from Google Cloud Console\n"
                "For Railway deployment: Set GOOGLE_CREDENTIALS_JSON environment variable with the JSON content"
            )
        
        print(f"[AUTH] Credentials structure: {list(creds_data.keys())}")
        
        # Determine redirect URI based on environment
        if IS_RAILWAY:
            redirect_uri = f"https://{os.environ.get('RAILWAY_PUBLIC_DOMAIN')}/oauth2callback"
        else:
            redirect_uri = 'http://localhost:8080/oauth2callback'
        
        print(f"[AUTH] Using redirect URI: {redirect_uri}")
        
        # Create flow from credentials dict
        flow = Flow.from_client_config(
            creds_data,
            scopes=SCOPES,
            redirect_uri=redirect_uri,
            state=None
        )
        print("[AUTH] OAuth flow created successfully")
        return flow
    except json.JSONDecodeError as e:
        print(f"[AUTH ERROR] JSON parse error: {str(e)}")
        raise ValueError(f"Credentials JSON is not valid: {str(e)}")
    except Exception as e:
        print(f"[AUTH ERROR] {str(e)}")
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
