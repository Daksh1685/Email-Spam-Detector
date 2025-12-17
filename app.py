from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import warnings
from auth import get_google_flow, save_credentials, load_credentials, clear_credentials
from gmail_service import get_emails, get_email_by_id, mark_spam, delete_email
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

warnings.filterwarnings('ignore')

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'your-secret-key-change-this'
Session(app)

clf = None

def train_model():
    global clf
    
    df = pd.read_csv("https://raw.githubusercontent.com/Apaulgithub/oibsip_taskno4/main/spam.csv", encoding='ISO-8859-1')
    
    df.rename(columns={"v1": "Category", "v2": "Message"}, inplace=True)
    df.drop(columns={'Unnamed: 2','Unnamed: 3','Unnamed: 4'}, inplace=True, errors='ignore')
    df['Spam'] = df['Category'].apply(lambda x: 1 if x == 'spam' else 0)
    
    clf = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('nb', MultinomialNB())
    ])
    
    clf.fit(df.Message, df.Spam)
    
    return clf

@app.route('/')
def index():
    credentials = load_credentials()
    if credentials:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login')
def login():
    """Initiate Google OAuth login"""
    try:
        import os
        creds_path = os.path.join(os.getcwd(), 'credentials.json')
        
        if not os.path.exists(creds_path):
            return render_template('login_error.html', 
                error="credentials.json not found",
                message=f"Please download credentials.json from Google Cloud Console and place it in: {creds_path}"), 400
        
        # Verify the credentials.json can be read and parsed
        try:
            with open(creds_path, 'r') as f:
                creds_data = json.load(f)
            if 'web' not in creds_data:
                raise ValueError("Missing 'web' section in credentials.json")
            web_config = creds_data['web']
            required_fields = ['client_id', 'client_secret', 'auth_uri', 'token_uri']
            for field in required_fields:
                if field not in web_config:
                    raise ValueError(f"Missing required field: {field}")
        except json.JSONDecodeError as e:
            return render_template('login_error.html',
                error="Invalid credentials.json format",
                message=f"The credentials.json file is not valid JSON: {str(e)}"), 400
        except ValueError as e:
            return render_template('login_error.html',
                error="Invalid credentials.json structure",
                message=f"The credentials.json file is missing required fields: {str(e)}"), 400
        
        flow = get_google_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # Store the flow state in session for later use
        session['oauth_state'] = state
        session.modified = True
        print(f"[LOGIN] Successfully created authorization URL with state: {state}")
        return redirect(authorization_url)
    except Exception as e:
        import traceback
        error_msg = str(e)
        full_traceback = traceback.format_exc()
        print(f"[LOGIN ERROR] {error_msg}")
        print(f"[LOGIN TRACEBACK]\n{full_traceback}")
        
        # Check for specific Google API errors
        if "invalid_client" in error_msg.lower():
            return render_template('login_error.html',
                error="Invalid credentials.json",
                message="Google rejected your credentials (invalid_client). Possible causes:<br>1. OAuth consent screen not configured<br>2. Client credentials need to be regenerated<br>3. Check redirect URI is exactly: http://localhost:8080/oauth2callback"), 400
        elif "client_id" in error_msg.lower() or "client_secret" in error_msg.lower():
            return render_template('login_error.html',
                error="Invalid credentials.json",
                message="Your credentials.json file is not valid. Check that client_id and client_secret are correct."), 400
        
        return render_template('login_error.html',
            error="Login Error",
            message=f"{error_msg}\n\nCheck the server logs for more details."), 500

@app.route('/oauth2callback')
def oauth2callback():
    """Handle Google OAuth callback"""
    try:
        from google_auth_oauthlib.flow import Flow
        import json
        
        # Recreate the flow to handle the callback
        flow = get_google_flow()
        
        # Fetch token using the authorization response
        authorization_response = request.url
        print(f"[OAUTH2] Handling callback with URL: {authorization_response}")
        
        flow.fetch_token(authorization_response=authorization_response)
        
        # Save credentials
        credentials = flow.credentials
        save_credentials(credentials)
        
        print(f"[OAUTH2] Successfully saved credentials")
        
        return redirect(url_for('dashboard'))
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"[OAUTH2 ERROR] {error_msg}")
        traceback.print_exc()
        
        return render_template('login_error.html',
            error="OAuth Callback Error",
            message=f"Failed to complete authentication: {error_msg}"), 400

@app.route('/logout')
def logout():
    """Logout user"""
    clear_credentials()
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """User dashboard with emails"""
    credentials = load_credentials()
    if not credentials:
        return redirect(url_for('login'))
    
    emails = get_emails(credentials, max_results=20)
    return render_template('dashboard.html', emails=emails, demo_mode=False)

@app.route('/email/<email_id>')
def view_email(email_id):
    """View single email"""
    credentials = load_credentials()
    if not credentials:
        return redirect(url_for('login'))
    
    email_data = get_email_by_id(credentials, email_id)
    return render_template('email_detail.html', email=email_data)

@app.route('/api/emails', methods=['GET'])
def get_emails_api():
    """API endpoint to get emails"""
    try:
        credentials = load_credentials()
        if not credentials:
            return jsonify({'error': 'Not authenticated'}), 401
        
        limit = request.args.get('limit', 10, type=int)
        emails = get_emails(credentials, max_results=limit)
        return jsonify({'success': True, 'emails': emails})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/load-more', methods=['GET'])
def load_more_emails():
    """API endpoint to load more emails with pagination"""
    try:
        credentials = load_credentials()
        if not credentials:
            return jsonify({'error': 'Not authenticated'}), 401
        
        offset = request.args.get('offset', 0, type=int)
        limit = 20  # Load 20 emails at a time
        
        emails = get_emails(credentials, max_results=limit, offset=offset)
        
        return jsonify({
            'success': True, 
            'emails': emails,
            'offset': offset,
            'count': len(emails)
        })
    except Exception as e:
        print(f"[LOAD_MORE ERROR] {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mark-spam/<email_id>', methods=['POST'])
def api_mark_spam(email_id):
    """API endpoint to mark email as spam"""
    try:
        credentials = load_credentials()
        if not credentials:
            return jsonify({'error': 'Not authenticated'}), 401
        
        success = mark_spam(credentials, email_id)
        if success:
            return jsonify({'success': True, 'message': 'Email marked as spam'})
        else:
            return jsonify({'success': False, 'error': 'Failed to mark email'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/delete/<email_id>', methods=['POST'])
def api_delete_email(email_id):
    """API endpoint to delete email"""
    try:
        credentials = load_credentials()
        if not credentials:
            return jsonify({'error': 'Not authenticated'}), 401
        
        success = delete_email(credentials, email_id)
        if success:
            return jsonify({'success': True, 'message': 'Email deleted'})
        else:
            return jsonify({'success': False, 'error': 'Failed to delete email'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.json
        email_text = data.get('email_text', '').strip()
        
        if not email_text:
            return jsonify({
                'success': False,
                'error': 'Please enter an email text'
            }), 400
        
        prediction = clf.predict([email_text])[0]
        confidence = max(clf.predict_proba([email_text])[0]) * 100
        
        if prediction == 0:
            result = "Ham"
            message = "✓ This is a legitimate email"
            color = "success"
        else:
            result = "Spam"
            message = "✗ This email is likely spam"
            color = "danger"
        
        return jsonify({
            'success': True,
            'result': result,
            'message': message,
            'confidence': f"{confidence:.2f}",
            'color': color
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Error processing email: {str(e)}"
        }), 500

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'model': 'Multinomial Naive Bayes',
        'accuracy': '98.21%',
        'precision': '98.26%',
        'recall': '88.48%',
        'f1_score': '93.11%',
        'training_samples': 5572
    })

if __name__ == '__main__':
    print("Training spam detection model...")
    train_model()
    print("Model trained successfully!")
    print("Starting Flask application...")
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
