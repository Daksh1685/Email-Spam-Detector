# Email Spam Detection with Machine Learning

A comprehensive email spam detection system using machine learning, featuring both a Python script and an interactive web interface.

## Project Overview

This project implements a spam detection system using a **Multinomial Naive Bayes** classifier trained on 5,572 labeled emails. It achieves **98.21% accuracy** on the test dataset.

## Features

✅ **Real-Time Detection** - Instant spam/ham classification  
✅ **High Accuracy** - 98.21% test accuracy  
✅ **Web Interface** - Beautiful and intuitive UI  
✅ **Confidence Scores** - Probability-based predictions  
✅ **Privacy Focused** - No data storage or tracking  
✅ **Easy to Use** - Simple and straightforward interface  

## Performance Metrics

| Metric | Score |
|--------|-------|
| Test Accuracy | 98.21% |
| Precision | 98.26% |
| Recall | 88.48% |
| F1-Score | 93.11% |
| ROC-AUC | 0.9714 |

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Navigate to the project directory:**
```bash
cd "c:\Users\DAKSH\OneDrive\Documents\Gen_ai_project"
```

2. **Create a virtual environment (already created):**
```bash
.\.venv\Scripts\python.exe -m venv .venv
```

3. **Install required packages:**
```bash
.\.venv\Scripts\pip.exe install numpy pandas matplotlib seaborn scikit-learn wordcloud flask
```

## Usage

### Option 1: Run Python Script (Standalone)

Run the complete ML pipeline script:

```bash
.\.venv\Scripts\python.exe Email_Spam_Detection_with_Machine_Learning.py
```

**What this does:**
- Loads and explores the dataset
- Visualizes spam vs ham distribution
- Creates word clouds of spam messages
- Trains the Multinomial Naive Bayes model
- Generates evaluation metrics and confusion matrices
- Tests the spam detection on sample emails
- Saves visualization charts (PNG files)

### Option 2: Run Web Application (Interactive UI)

Start the Flask web server:

```bash
.\.venv\Scripts\python.exe app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

**Features available in web UI:**
- **Home Page** - Interactive email analysis tool
- **About Page** - Project information and performance metrics
- **Real-time Analysis** - Instant spam/ham classification
- **Confidence Scores** - Visual confidence percentage
- **Responsive Design** - Works on desktop, tablet, and mobile

## Project Structure

```
Gen_ai_project/
├── Email_Spam_Detection_with_Machine_Learning.py  # Main ML script
├── Email_Spam_Detection_with_Machine_Learning.ipynb # Jupyter notebook
├── app.py                                          # Flask web application
│
├── templates/
│   ├── index.html                                  # Home page
│   └── about.html                                  # About page
│
├── static/
│   ├── css/
│   │   └── style.css                              # Custom CSS styles
│   └── js/
│       └── script.js                              # JavaScript functionality
│
├── confusion_matrix.png                           # Model evaluation visualization
├── roc_curve.png                                  # ROC curve plot
├── spam_ham_distribution.png                      # Data distribution chart
└── spam_wordcloud.png                             # Word cloud visualization
```

## How the System Works

1. **Data Loading** - Loads 5,572 labeled emails from GitHub
2. **Preprocessing** - Cleans and prepares text data
3. **Feature Extraction** - Converts text to numerical features using CountVectorizer
4. **Model Training** - Trains Multinomial Naive Bayes classifier
5. **Classification** - Predicts whether email is spam or ham
6. **Output** - Returns result with confidence score

## Dataset Information

- **Total Emails:** 5,572
- **Spam Emails:** 747 (13.41%)
- **Ham Emails:** 4,825 (86.59%)
- **Duplicate Rows:** 403 (removed)
- **Source:** [Kaggle Spam Dataset](https://raw.githubusercontent.com/Apaulgithub/oibsip_taskno4/main/spam.csv)

## Common Spam Keywords Detected

From the word cloud analysis, the most common spam keywords are:
- `free`
- `call`
- `text`
- `txt`
- `now`
- `click`
- `prize`
- `limited`

## Technologies Used

### Backend
- **Python 3.x** - Programming language
- **Flask** - Web framework
- **scikit-learn** - Machine learning library
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib & seaborn** - Data visualization
- **wordcloud** - Word cloud generation

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **JavaScript** - Interactivity
- **Bootstrap 5** - UI framework
- **Bootstrap Icons** - Icon library

## API Endpoints

### POST /detect
Analyzes an email for spam

**Request:**
```json
{
  "email_text": "Your email content here"
}
```

**Response:**
```json
{
  "success": true,
  "result": "Ham",
  "message": "✓ This is a legitimate email",
  "confidence": "99.45",
  "color": "success"
}
```

### GET /api/stats
Returns model statistics

**Response:**
```json
{
  "model": "Multinomial Naive Bayes",
  "accuracy": "98.21%",
  "precision": "98.26%",
  "recall": "88.48%",
  "f1_score": "93.11%",
  "training_samples": 5572
}
```

## Example Usage

### In Web UI:
1. Go to http://localhost:5000
2. Paste email text in the textarea
3. Click "Analyze Email"
4. View the result with confidence score

### Sample Test Emails:

**Spam Examples:**
- "Free Tickets for IPL! Click here to claim!"
- "You have won a free prize. Limited time offer!"
- "Limited time offer - Get 50% off now!"

**Ham Examples:**
- "Hi, How are you doing?"
- "Meeting scheduled for tomorrow at 2 PM"
- "Can we connect for coffee this weekend?"

## Keyboard Shortcuts

- **Ctrl + Enter** - Submit form
- **Escape** - Close result and reset form
- **Double-click** - Fill sample text in textarea

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution:** Install missing packages
```bash
.\.venv\Scripts\pip.exe install numpy pandas matplotlib seaborn scikit-learn wordcloud flask
```

### Issue: Port 5000 already in use
**Solution:** Stop the previous process or use a different port by modifying `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Network error when loading dataset
**Solution:** Check your internet connection. The script downloads data from GitHub.

## Performance Optimization Tips

1. **Faster Inference:** The model uses CountVectorizer which is efficient for text processing
2. **Memory Efficient:** Suitable for running on machines with limited resources
3. **Real-time Analysis:** Average prediction time < 100ms

## Future Enhancements

- [ ] Add email attachment analysis
- [ ] Implement more ML models (SVM, Random Forest, Neural Networks)
- [ ] Add user authentication
- [ ] Store email analysis history
- [ ] Implement real-time retraining
- [ ] Add spam report functionality
- [ ] Support multiple languages

## Ethical Considerations

- ✓ Privacy Protected - No data storage
- ✓ Fair Classification - Trained on balanced dataset
- ✓ Transparency - Clear confidence scores
- ✓ Security - No sensitive data handling

## Author

**Email Spam Detection System**

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Dataset source: [Kaggle](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)
- Machine Learning framework: [scikit-learn](https://scikit-learn.org/)
- Web framework: [Flask](https://flask.palletsprojects.com/)
- UI Framework: [Bootstrap](https://getbootstrap.com/)

## Support

For questions or issues, please refer to the About page in the web interface or review the project documentation.

---

**Last Updated:** November 28, 2025  
**Version:** 1.0.0
