📧 Email Spam Detector
🔍 Project Overview

The Email Spam Detector is a Machine Learning–based system that classifies emails as Spam or Not Spam (Ham) using Natural Language Processing (NLP).
It helps users automatically filter unwanted and malicious emails and can be connected to a user’s personal email account.

🎯 Problem Statement

Users receive a large number of spam emails such as advertisements and phishing messages.
Manual filtering is inefficient.
This project automates spam detection using Machine Learning for better accuracy and safety.

🛠️ Technologies Used

Language: Python

ML Model: Naive Bayes

NLP: Text Preprocessing

Feature Extraction: TF-IDF

Framework: Flask

Frontend: HTML, CSS

Dataset: SMS Spam Collection (Kaggle)

⚙️ System Flow
Email Input → Text Preprocessing → TF-IDF → Naive Bayes → Spam / Ham

🧠 Working

Email text is taken as input (manual or personal email).

Text is cleaned using NLP techniques.

TF-IDF converts text into numerical features.

Naive Bayes classifies the email as Spam or Ham.

🚀 Features

Automatic spam detection

Real-time email classification

Simple and user-friendly interface

Can connect to personal email accounts

📈 Result

Achieved high accuracy in spam detection

Naive Bayes performed efficiently for text classification

▶️ How to Run
git clone https://github.com/Daksh1685/Email-Spam-Detector
cd Email-Spam-Detector
pip install -r requirements.txt
python app.py


Open:

http://127.0.0.1:5000/
