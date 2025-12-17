# Email Spam Detector with Gmail Integration 📧

A machine learning-powered email spam detection system with **Google Gmail API integration**. Detect spam with 98.21% accuracy and manage your Gmail inbox directly from the web interface.

## ✨ Features

### Core Spam Detection
- 🤖 **98.21% Accurate** - Trained on 5,572 emails
- ⚡ **Lightning Fast** - Real-time analysis
- 📊 **Confidence Scoring** - Know how certain we are
- 🔒 **100% Private** - No email storage

### Gmail Integration (NEW!)
- 🔐 **Google OAuth Login** - Secure authentication
- 📧 **Gmail Inbox View** - See all your emails
- 🔍 **Analyze Emails** - Check for spam directly
- 🗑️ **Email Management** - Delete or mark as spam
- 📱 **Responsive Design** - Works on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Account (for Gmail integration)
- Google Cloud Project with Gmail API enabled

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Gen_ai_project
```

2. **Create virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Google API** (see detailed guide below)
- Download credentials.json from Google Cloud Console
- Save in project root directory

5. **Run the application**
```bash
python app.py
```

6. **Access the app**
- Open `http://localhost:8080` in your browser
- Click "Sign in with Google"
- Start analyzing emails!

## 🔐 Google API Setup

### Detailed Setup Instructions

See **[GOOGLE_API_SETUP.md](GOOGLE_API_SETUP.md)** for complete step-by-step instructions.

**Quick Summary:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable Gmail API
4. Create OAuth 2.0 Web Application credentials
5. Add redirect URI: `http://localhost:8080/oauth2callback`
6. Download JSON and save as `credentials.json`
7. Run the app!

## 📁 Project Structure

```
.
├── app.py                          # Main Flask application
├── auth.py                         # Google OAuth authentication
├── gmail_service.py                # Gmail API operations
├── Email_Spam_Detection_...py      # Data analysis scripts
├── Email_Analysis_Report.py        # Analysis utilities
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku deployment
├── static/
│   ├── css/style.css              # Styling
│   └── js/script.js               # Frontend logic
├── templates/
│   ├── index.html                 # Home page with login
│   ├── dashboard.html             # Email inbox
│   ├── email_detail.html          # Email viewer
│   ├── about.html                 # About page
│   └── contact.html               # Contact page
├── GOOGLE_API_SETUP.md            # Google API setup guide
├── GOOGLE_API_INTEGRATION_SUMMARY.md
├── QUICK_START.md                 # Quick start guide
├── .gitignore                     # Git ignore file
└── credentials.json               # (Create from Google Cloud - NOT in repo)
```

## 🛣️ API Routes

### Authentication Routes
- `GET /` - Home page (redirects to dashboard if logged in)
- `GET /login` - Initiate Google OAuth login
- `GET /oauth2callback` - OAuth callback handler
- `GET /logout` - Logout and clear session

### Dashboard Routes
- `GET /dashboard` - Email inbox view
- `GET /email/<email_id>` - View single email

### Detection Routes
- `POST /detect` - Analyze email for spam
  - Body: `{"email_text": "email content"}`
  - Response: `{"success": true, "result": "Ham|Spam", "confidence": "XX.XX", "message": "..."}`

### API Routes
- `GET /api/emails` - Get emails (query param: `limit`)
- `POST /api/mark-spam/<email_id>` - Mark email as spam
- `POST /api/delete/<email_id>` - Delete email
- `GET /api/stats` - Get model statistics

## 🧠 Machine Learning Model

### Algorithm
- **Type:** Multinomial Naive Bayes
- **Training Data:** 5,572 emails
- **Accuracy:** 98.21%
- **Precision:** 98.26%
- **Recall:** 88.48%
- **F1-Score:** 93.11%

### How It Works
1. Extract features using CountVectorizer
2. Train Multinomial Naive Bayes classifier
3. Predict spam probability
4. Return result with confidence score

## 📊 Usage Examples

### Analyze Email via Web Interface
1. Login with Google
2. View emails in dashboard
3. Click "Analyze" on any email
4. See spam detection result with confidence

### Manual Email Analysis
1. Go to home page
2. Paste email content
3. Click "Analyze Email"
4. Get instant spam detection result

### Use Email Management
1. From dashboard, click email to view full content
2. Click "Analyze for Spam" to check
3. Click "Mark as Spam" to categorize
4. Click "Delete" to remove from inbox

## 🔒 Security Features

- ✅ **OAuth 2.0** - No password storage
- ✅ **Token Encryption** - Credentials securely stored
- ✅ **Read-Only Access** - Gmail API limited to reading emails
- ✅ **Session Management** - Automatic logout
- ✅ **HTTPS Ready** - For production deployment

## 📱 Responsive Design

- ✨ Bootstrap 5 framework
- 📱 Mobile-friendly interface
- 🎯 Clean, intuitive design
- ⚡ Fast performance

## 🚀 Deployment

### Heroku Deployment
```bash
# Login to Heroku
heroku login

# Create app
heroku create <app-name>

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Docker Deployment
```bash
docker build -t email-spam-detector .
docker run -p 8080:8080 email-spam-detector
```

### Environment Variables
- `PORT` - Server port (default: 8080)
- `FLASK_ENV` - development/production
- Store credentials securely (not in environment)

## 🛠️ Development

### Running Tests
```bash
pytest
```

### Code Style
```bash
# Format code
black .

# Check style
flake8 .
```

### Enable Debug Mode (Development Only)
Edit `app.py`:
```python
app.run(debug=True, ...)
```

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - 5-minute quick start
- **[GOOGLE_API_SETUP.md](GOOGLE_API_SETUP.md)** - Detailed Google API setup
- **[GOOGLE_API_INTEGRATION_SUMMARY.md](GOOGLE_API_INTEGRATION_SUMMARY.md)** - Technical details

## 🐛 Troubleshooting

### Issue: credentials.json not found
**Solution:** Download from Google Cloud Console and save in project root

### Issue: Gmail API not enabled
**Solution:** Go to Google Cloud Console > APIs & Services > Enable Gmail API

### Issue: Redirect URI mismatch
**Solution:** Update Google Cloud Console settings to match your redirect URI

### Issue: Can't login
**Solution:** Check internet, clear cookies, verify credentials.json is valid JSON

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Daksh Chaurasia** and Team

## 🙏 Acknowledgments

- Dataset from [Kaggle SMS Spam Collection](https://www.kaggle.com/uciml/sms-spam-collection-dataset)
- Google Gmail API documentation
- Flask framework
- Bootstrap for UI components

## 📞 Contact

- **GitHub:** [@Daksh1685](https://github.com/Daksh1685)
- **Email:** [Your email here]

---

## 📈 What's Included

- Machine Learning spam detection (98.21% accurate)
- Gmail integration with OAuth login
- Email inbox management
- Individual email analysis
- Email deletion and spam marking
- Responsive web interface
- Complete API endpoints
- Comprehensive documentation

## 🎯 Future Enhancements

- [ ] Email filtering and search
- [ ] Bulk email analysis
- [ ] Email templates
- [ ] Schedule emails
- [ ] Email attachments handling
- [ ] Advanced analytics dashboard
- [ ] Mobile app
- [ ] Email categorization

---

**Ready to get started?** See [QUICK_START.md](QUICK_START.md) for installation instructions.

Happy Spam Detection! 🎉
