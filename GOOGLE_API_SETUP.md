# Google API Setup Guide

## How to Set Up Google OAuth Integration

Follow these steps to enable Google Gmail API integration for your Email Spam Detector:

### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown and select "New Project"
3. Enter project name (e.g., "Email Spam Detector") and click "Create"

### Step 2: Enable Gmail API
1. In the Cloud Console, go to APIs & Services > Library
2. Search for "Gmail API"
3. Click on Gmail API and then click "Enable"

### Step 3: Create OAuth 2.0 Credentials
1. Go to APIs & Services > Credentials
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. Select "Web application"
4. Add authorized redirect URIs:
   - `http://localhost:8080/oauth2callback`
   - `http://localhost:8080`
5. Click "Create"
6. Download the JSON file

### Step 4: Configure Your Application
1. Save the downloaded JSON file as `credentials.json` in your project root directory
2. The file should look like this:
```json
{
  "web": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": [
      "http://localhost:8080/oauth2callback"
    ]
  }
}
```

### Step 5: Install Dependencies
Run the following command to install required packages:
```bash
pip install -r requirements.txt
```

### Step 6: Update Flask Secret Key
Edit `app.py` and change the secret key:
```python
app.secret_key = 'your-very-secure-secret-key-here'  # Change this to a random string
```

### Step 7: Run the Application
```bash
python app.py
```

### Step 8: Use the Application
1. Navigate to `http://localhost:8080`
2. Click "Sign in with Google"
3. Authorize the application to access your Gmail
4. View and analyze your emails from the dashboard

## Features After Setup

- ✅ **Gmail Integration**: View emails directly from your Gmail inbox
- ✅ **Email Analysis**: Run spam detection on individual emails
- ✅ **Mark as Spam**: Mark emails as spam in Gmail
- ✅ **Delete Emails**: Delete emails from the dashboard
- ✅ **Secure**: Only reads emails, no storage on our servers

## Troubleshooting

### Issue: "credentials.json not found"
- Make sure you've downloaded the OAuth credentials file and saved it as `credentials.json` in the project root

### Issue: "Redirect URI mismatch"
- Ensure the redirect URI in Google Cloud Console matches exactly: `http://localhost:8080/oauth2callback`

### Issue: "Gmail API not enabled"
- Go to Google Cloud Console > APIs & Services and enable the Gmail API

### Issue: "Permission denied"
- Make sure you granted the app permission to read Gmail during OAuth authentication

## Production Deployment

For production deployment:
1. Update `redirect_uri` to your domain
2. Change `app.secret_key` to a secure random key
3. Update Flask config to use a proper session backend (not filesystem)
4. Store credentials securely
5. Use environment variables for sensitive data
