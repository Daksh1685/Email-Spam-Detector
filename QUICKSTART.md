# Quick Start Guide

## Running the Email Spam Detection System

### Method 1: Python Script (Analysis Only)

```powershell
cd "c:\Users\DAKSH\OneDrive\Documents\Gen_ai_project"
.\.venv\Scripts\python.exe Email_Spam_Detection_with_Machine_Learning.py
```

**Output:**
- Displays dataset analysis
- Shows model performance metrics
- Tests spam detection on sample emails
- Generates visualization charts

---

### Method 2: Web Application (Interactive UI)

```powershell
cd "c:\Users\DAKSH\OneDrive\Documents\Gen_ai_project"
.\.venv\Scripts\python.exe app.py
```

**Then:**
1. Open browser
2. Go to: `http://localhost:5000`
3. Paste email text
4. Click "Analyze Email"
5. View result with confidence score

---

## What's Included

✅ **Python Script** - Standalone ML pipeline  
✅ **Web Application** - Interactive UI with Flask  
✅ **HTML Templates** - Modern responsive pages  
✅ **CSS Styling** - Beautiful and professional design  
✅ **JavaScript** - Dynamic user interactions  
✅ **Documentation** - Comprehensive README  

## Features

### Web UI Features:
- Real-time email analysis
- Confidence percentage display
- Color-coded results (success/danger)
- Responsive mobile design
- About page with model statistics
- Smooth animations and transitions

### Python Script Features:
- Complete dataset exploration
- Data visualization (charts, word clouds)
- Model training and evaluation
- Confusion matrix and ROC curves
- Classification reports
- Sample email testing

## Files Structure

```
Project Folder/
├── Email_Spam_Detection_with_Machine_Learning.py  ← Run this for analysis
├── app.py                                          ← Run this for web UI
├── templates/
│   ├── index.html                                  ← Home page
│   └── about.html                                  ← About page
├── static/
│   ├── css/style.css                              ← Custom styling
│   └── js/script.js                               ← JavaScript logic
├── README.md                                      ← Full documentation
└── QUICKSTART.md                                  ← This file
```

## Keyboard Shortcuts (Web UI)

| Shortcut | Action |
|----------|--------|
| Ctrl + Enter | Submit form |
| Escape | Close result |
| Double-click textarea | Fill sample text |

## Performance

- **Accuracy:** 98.21%
- **Processing Speed:** < 100ms per email
- **Model:** Multinomial Naive Bayes
- **Training Data:** 5,572 emails

## Troubleshooting

### Issue: "ModuleNotFoundError"
```powershell
.\.venv\Scripts\pip.exe install numpy pandas matplotlib seaborn scikit-learn wordcloud flask
```

### Issue: Port 5000 in use
Edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### Issue: Cannot download dataset
Check internet connection - data is loaded from GitHub

## Support

- See README.md for detailed documentation
- Check About page in web UI for statistics
- Review generated charts for model performance

---

**Ready to go!** Choose your preferred method above and start detecting spam! 🚀
