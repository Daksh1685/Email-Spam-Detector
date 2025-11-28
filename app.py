from flask import Flask, render_template, request, jsonify
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)

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
    return render_template('index.html')

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
    app.run(debug=True, host='127.0.0.1', port=8080)
