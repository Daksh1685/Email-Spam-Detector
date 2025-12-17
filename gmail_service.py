import base64
import email
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pickle
import os
from demo_emails import DEMO_EMAILS

TOKEN_PICKLE_FILE = 'token.pickle'
DEMO_MODE = False  # Set to False to use real Gmail API

def get_gmail_service(credentials):
    """Build Gmail API service"""
    if DEMO_MODE:
        return None
    return build('gmail', 'v1', credentials=credentials)

def get_emails(credentials, max_results=10):
    """Fetch emails from Gmail or return demo emails in demo mode"""
    try:
        if DEMO_MODE:
            # Return demo emails
            return DEMO_EMAILS[:max_results]
        
        service = get_gmail_service(credentials)
        results = service.users().messages().list(userId='me', maxResults=max_results, q='').execute()
        messages = results.get('messages', [])
        
        emails = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            headers = msg['payload']['headers']
            
            email_data = {
                'id': message['id'],
                'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject'),
                'from': next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown'),
                'date': next((h['value'] for h in headers if h['name'] == 'Date'), ''),
                'snippet': msg['snippet']
            }
            
            # Get email body
            try:
                if 'parts' in msg['payload']:
                    email_data['body'] = get_message_body(msg['payload']['parts'])
                else:
                    email_data['body'] = base64.urlsafe_b64decode(msg['payload']['body'].get('data', '')).decode('utf-8')
            except:
                email_data['body'] = email_data['snippet']
            
            emails.append(email_data)
        
        return emails
    except Exception as e:
        print(f"Error fetching emails: {str(e)}")
        if DEMO_MODE:
            return DEMO_EMAILS[:max_results]
        return []

def get_message_body(parts):
    """Extract message body from email parts"""
    for part in parts:
        if part['mimeType'] == 'text/plain':
            try:
                return base64.urlsafe_b64decode(part['body'].get('data', '')).decode('utf-8')
            except:
                return part['body'].get('data', '')
    return ''

def get_email_by_id(credentials, message_id):
    """Get a specific email by ID"""
    try:
        if DEMO_MODE:
            # Find demo email with matching ID
            for email_data in DEMO_EMAILS:
                if email_data['id'] == message_id:
                    return email_data
            return None
        
        service = get_gmail_service(credentials)
        msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        headers = msg['payload']['headers']
        
        email_data = {
            'id': message_id,
            'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject'),
            'from': next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown'),
            'to': next((h['value'] for h in headers if h['name'] == 'To'), ''),
            'date': next((h['value'] for h in headers if h['name'] == 'Date'), ''),
            'snippet': msg['snippet']
        }
        
        # Get email body
        try:
            if 'parts' in msg['payload']:
                email_data['body'] = get_message_body(msg['payload']['parts'])
            else:
                email_data['body'] = base64.urlsafe_b64decode(msg['payload']['body'].get('data', '')).decode('utf-8')
        except:
            email_data['body'] = email_data['snippet']
        
        return email_data
    except Exception as e:
        print(f"Error fetching email: {str(e)}")
        return None

def delete_email(credentials, message_id):
    """Delete an email"""
    try:
        if DEMO_MODE:
            print(f"[DEMO MODE] Would delete email: {message_id}")
            return True
        
        service = get_gmail_service(credentials)
        service.users().messages().delete(userId='me', id=message_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting email: {str(e)}")
        return False

def mark_spam(credentials, message_id):
    """Mark email as spam"""
    try:
        if DEMO_MODE:
            print(f"[DEMO MODE] Would mark as spam: {message_id}")
            return True
        
        service = get_gmail_service(credentials)
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'addLabelIds': ['SPAM']}
        ).execute()
        return True
    except Exception as e:
        print(f"Error marking spam: {str(e)}")
        return False
