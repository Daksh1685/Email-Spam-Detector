# 🚀 Quick Start - Google OAuth Setup (3 Minutes)

## ❌ The Problem
You're seeing: **"Access blocked: Authorization Error (Error 401: invalid_client)"**

## ✅ The Solution

### 1️⃣ Get Real Credentials from Google
Go to: https://console.cloud.google.com/

**Quick steps:**
- Create/Select Project
- Enable **Gmail API** (search for it)
- Go to **Credentials** → **Create** → **OAuth 2.0 Client ID** → **Web application**
- Add redirect URI: `http://localhost:8080/oauth2callback`
- Download the JSON file

### 2️⃣ Update credentials.json
- Copy the entire downloaded JSON content
- Paste it into `credentials.json` in your project folder
- **Replace everything** in the file
- Save

### 3️⃣ Restart the App
```bash
python app.py
```

### 4️⃣ Try Login Again
Click "Sign in with Google Mail" at http://localhost:8080

---

## 📋 Checklist
- [ ] Created Google Cloud project
- [ ] Enabled Gmail API
- [ ] Created OAuth 2.0 Web Application credentials
- [ ] Added `http://localhost:8080/oauth2callback` to redirect URIs
- [ ] Downloaded credentials JSON
- [ ] Updated `credentials.json` with real values
- [ ] Restarted Flask app
- [ ] Tried login again

---

## 🆘 Still Not Working?

### Check if credentials.json has real values:
```json
{
  "web": {
    "client_id": "NOT_YOUR-CLIENT-ID.apps.googleusercontent.com",  ← Must have real ID
    "client_secret": "NOT_YOUR-CLIENT-SECRET",  ← Must have real secret
    ...
  }
}
```

### If you see placeholder text like:
- `your-client-id` ← ❌ WRONG
- `your-client-secret` ← ❌ WRONG
- `REPLACE_WITH_...` ← ❌ WRONG

**You need to get real credentials from Google Cloud Console!**

---

## 📖 Detailed Guide
See `GOOGLE_OAUTH_SETUP.md` for step-by-step screenshots and more help.

---

**Still stuck?** Check the Google OAuth Console error logs for more details on what's wrong.
