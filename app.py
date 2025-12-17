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
        if not os.path.exists('credentials.json'):
            return render_template('login_error.html', 
                error="credentials.json not found",
                message="Please download credentials.json from Google Cloud Console and place it in the project root directory."), 400
        
        flow = get_google_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        session['state'] = state
        return redirect(authorization_url)
    except Exception as e:
        error_msg = str(e)
        if "Invalid client" in error_msg or "client_id" in error_msg:
            return render_template('login_error.html',
                error="Invalid credentials.json",
                message="Your credentials.json file is not valid. Please download a new one from Google Cloud Console."), 400
        return render_template('login_error.html',
            error="Login Error",
            message=error_msg), 500

@app.route('/oauth2callback')
def oauth2callback():
    """Handle Google OAuth callback"""
    try:
        state = session['state']
        flow = get_google_flow()
        flow.fetch_token(authorization_response=request.url)
        
        credentials = flow.credentials
        save_credentials(credentials)
        
        return redirect(url_for('dashboard'))
    except Exception as e:
        return jsonify({'error': f"Authentication failed: {str(e)}"}), 500

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
