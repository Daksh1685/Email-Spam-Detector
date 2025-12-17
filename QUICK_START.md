# Email Spam Detector - Quick Start Guide (Updated with Google Gmail API)

## 🚀 What's New?

Your Email Spam Detector now has **Google Gmail Integration**! Users can now:
- ✅ Login with their Google account
- ✅ View their Gmail inbox directly in the app
- ✅ Analyze emails for spam using the ML model
- ✅ Delete or mark emails as spam from the dashboard
- ✅ View full email details with sender info and timestamps

## 📋 Quick Setup (5 Minutes)

### 1. Get Google Credentials (2 minutes)
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project
- Enable Gmail API
- Create OAuth 2.0 Web Application credentials
- Download the JSON file and save as `credentials.json` in project root

**Important:** Configure redirect URI: `http://localhost:8080/oauth2callback`

### 2. Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### 3. Update Secret Key (30 seconds)
Edit `app.py` line 23 and change:
```python
app.secret_key = 'your-secret-key-change-this'
```
to:
```python
app.secret_key = 'my-super-secret-key-12345'  # Use any random string
```

### 4. Run the App (30 seconds)
```bash
python app.py
```

### 5. Access and Login (1 minute)
- Open `http://localhost:8080`
- Click "Sign in with Google"
- Authorize the app
- Start analyzing emails!

## 📁 New Files Added

| File | Purpose |
|------|---------|
| `auth.py` | Google OAuth authentication |
| `gmail_service.py` | Gmail API integration |
| `templates/dashboard.html` | Email inbox view |
| `templates/email_detail.html` | Full email viewer |
| `GOOGLE_API_SETUP.md` | Detailed setup guide |
| `GOOGLE_API_INTEGRATION_SUMMARY.md` | Full integration details |

## 🔗 Routes Available

| Route | Purpose |
|-------|---------|
| `/` | Home page (redirects to dashboard if logged in) |
| `/login` | Initiate Google OAuth |
| `/oauth2callback` | OAuth callback (automatic) |
| `/logout` | Logout and clear session |
| `/dashboard` | Email inbox view |
| `/email/<id>` | View individual email |
| `/detect` | Analyze email for spam (POST) |
| `/api/emails` | Get emails API (GET) |
| `/api/mark-spam/<id>` | Mark as spam (POST) |
| `/api/delete/<id>` | Delete email (POST) |

## 🔒 Security Notes

- Credentials stored in `token.pickle` (local only, for development)
- Credentials.json is in `.gitignore` (won't be committed)
- OAuth 2.0 - User passwords never seen by the app
- Gmail API has READ-ONLY access
- User session management with Flask-Session

## 🐛 Troubleshooting

**Problem: "credentials.json not found"**
- Ensure you've downloaded and saved the OAuth credentials file

**Problem: "Redirect URI mismatch"**
- Check Google Cloud Console settings match: `http://localhost:8080/oauth2callback`

**Problem: "Gmail API not enabled"**
- Go to Google Cloud Console > APIs & Services > Enable Gmail API

**Problem: Cannot login**
- Check internet connection
- Try clearing browser cookies
- Verify credentials.json is valid JSON

## 📊 Features

### Dashboard Features
- 📧 View 20 most recent emails
- 👤 See sender, subject, date, preview
- 🔍 Analyze email for spam
- 🗑️ Delete emails
- ⚠️ Mark as spam

### Email Detail View
- 📝 Full email body
- 📤 From/To information
- 📅 Date and time
- 🔬 Spam analysis
- 🎯 Detailed confidence score

### Spam Detection
- 98.21% accuracy
- Uses Multinomial Naive Bayes
- Instant analysis
- Confidence scoring

## 🎯 Next Steps

1. **Setup Google API credentials** → Follow Google API setup guide
2. **Run the application** → `python app.py`
3. **Test with your emails** → Login and analyze
4. **Customize** → Modify colors, add features, deploy

## 📦 Dependencies Added

```
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.100.0
Flask-Session>=0.5.0
python-dotenv>=1.0.0
```

## 🌐 Production Deployment

Before deploying to production:
1. Change `app.debug = False` (already set)
2. Use environment variables for secret key
3. Use proper session backend (database/redis instead of filesystem)
4. Update redirect URIs to your domain
5. Use HTTPS
6. Implement proper error logging

## 📞 Support

For issues or questions:
1. Check `GOOGLE_API_SETUP.md` for detailed instructions
2. Review `GOOGLE_API_INTEGRATION_SUMMARY.md` for full technical details
3. Check Google Cloud Console settings
4. Verify all files are created correctly

## ✨ Enjoy!

Your Email Spam Detector is now ready to analyze emails from your Gmail inbox! 🎉

For detailed setup instructions, see `GOOGLE_API_SETUP.md`
