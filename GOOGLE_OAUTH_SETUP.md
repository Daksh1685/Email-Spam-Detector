# Google OAuth Setup Guide

## Error: "Access blocked: Authorization Error (Error 401: invalid_client)"

This error means your `credentials.json` file has placeholder values instead of real Google OAuth credentials.

---

## ✅ Complete Setup Instructions

### Step 1: Go to Google Cloud Console
1. Open: https://console.cloud.google.com/
2. Sign in with your Google account

### Step 2: Create a New Project
1. Click **"Select a Project"** (top left)
2. Click **"New Project"**
3. Enter Project Name: `Email Spam Detector`
4. Click **Create**
5. Wait for project creation to complete (1-2 minutes)

### Step 3: Enable Gmail API
1. Go to **APIs & Services** → **Library** (left sidebar)
2. Search for **"Gmail API"**
3. Click on **Gmail API**
4. Click **Enable**

### Step 4: Create OAuth 2.0 Credentials
1. Go to **APIs & Services** → **Credentials** (left sidebar)
2. Click **Create Credentials** → **OAuth 2.0 Client ID**
3. If prompted, configure OAuth consent screen first:
   - Choose **External**
   - Fill in required fields (App name, support email, etc.)
   - Click **Save and Continue**
   - Skip optional fields and click **Save and Continue** again
   - Click **Back to Dashboard**

4. Now create the OAuth credential again:
   - Click **Create Credentials** → **OAuth 2.0 Client ID**
   - Application Type: **Web application**
   - Name: `Email Spam Detector`
   
5. Under **Authorized redirect URIs**, add:
   ```
   http://localhost:8080/oauth2callback
   ```
   - Click **Add URI**
   
6. Click **Create**

### Step 5: Download Your Credentials
1. You'll see your OAuth 2.0 Client ID created
2. Find it in the Credentials table
3. Click the **Download icon** (⬇️) on the right
4. This downloads a JSON file

### Step 6: Update credentials.json
1. Open the downloaded JSON file
2. Copy all its contents
3. Go back to your project folder
4. Open `credentials.json`
5. Replace ALL the content with the downloaded JSON
6. **Save the file**

---

## Example of Valid credentials.json Format

```json
{
  "web": {
    "client_id": "123456789-abc123def456xyz789.apps.googleusercontent.com",
    "project_id": "email-spam-detector-12345",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSPX-abc123def456xyz789abc123",
    "redirect_uris": [
      "http://localhost:8080/oauth2callback"
    ]
  }
}
```

---

## ✅ After Setup

1. **Restart your Flask app**:
   ```bash
   python app.py
   ```

2. **Try logging in again** at `http://localhost:8080`

3. **Click "Sign in with Google Mail"**

4. **Grant permissions** when prompted

5. **You should now see your Gmail inbox!**

---

## Troubleshooting

### Still getting "invalid_client" error?
- ❌ Verify `client_id` doesn't say `your-client-id`
- ❌ Verify `client_secret` doesn't say `your-client-secret`
- ❌ Make sure you copied the ENTIRE JSON content
- ❌ Check the file is saved properly

### Getting "Redirect URI mismatch"?
- ✅ Make sure credentials.json has: `"http://localhost:8080/oauth2callback"`
- ✅ Check you're running on `localhost:8080` (not another port)

### Still not working?
- Delete `token.pickle` file (if exists)
- Restart the Flask app
- Try logging in again

---

## Important Notes

⚠️ **Never share your `credentials.json`** - it contains your secret credentials!

🔐 **Keep `client_secret` safe** - add to `.gitignore` if using git

✅ **Localhost only** - These credentials work only for local development

---

Need more help? Check Google Cloud Documentation:
https://developers.google.com/identity/protocols/oauth2
