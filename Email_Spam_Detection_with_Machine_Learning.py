import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, classification_report

from wordcloud import WordCloud, STOPWORDS

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import MultinomialNB

from sklearn.pipeline import Pipeline

import warnings
warnings.filterwarnings('ignore')

print("Loading dataset...")
df = pd.read_csv("https://raw.githubusercontent.com/Apaulgithub/oibsip_taskno4/main/spam.csv", encoding='ISO-8859-1')

print("\n" + "="*70)
print("1. DATASET FIRST VIEW")
print("="*70)
print(df.head())

print("\n" + "="*70)
print("2. DATASET INFO")
print("="*70)
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

print("\nDataset Info:")
df.info()

print("\nDuplicate rows:", df.duplicated().sum())
print("\nMissing values:")
print(df.isnull().sum())

print("\nDataset Columns:")
print(df.columns.tolist())

print("\nDataset Description:")
print(df.describe(include='all').round(2))

print("\nUnique values per column:")
for i in df.columns.tolist():
    print(f"No. of unique values in {i}: {df[i].nunique()}")

print("\n" + "="*70)
print("3. DATA WRANGLING")
print("="*70)

df.rename(columns={"v1": "Category", "v2": "Message"}, inplace=True)

df.drop(columns={'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'}, inplace=True)

df['Spam'] = df['Category'].apply(lambda x: 1 if x == 'spam' else 0)

print("\nUpdated Dataset:")
print(df.head())

print("\n" + "="*70)
print("4. DATA VISUALIZATION")
print("="*70)

print("\nChart 1: Distribution of Spam vs Ham Messages")
spread = df['Category'].value_counts()
print(spread)

plt.figure(figsize=(5, 5))
spread.plot(kind='pie', autopct='%1.2f%%', cmap='Set1')
plt.title('Distribution of Spam vs Ham')
plt.savefig('spam_ham_distribution.png', dpi=100, bbox_inches='tight')
print("Saved: spam_ham_distribution.png")

df_spam = df[df['Category'] == 'spam'].copy()

print("\nChart 2: Most Used Words in Spam Messages")
comment_words = ''
stopwords = set(STOPWORDS)

for val in df_spam.Message:
    val = str(val)
    tokens = val.split()
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
    comment_words += " ".join(tokens) + " "

wordcloud = WordCloud(width=1000, height=500,
                      background_color='white',
                      stopwords=stopwords,
                      min_font_size=10,
                      max_words=1000,
                      colormap='gist_heat_r').generate(comment_words)

plt.figure(figsize=(6, 6), facecolor=None)
plt.title('Most Used Words In Spam Messages', fontsize=15, pad=20)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig('spam_wordcloud.png', dpi=100, bbox_inches='tight')
print("Saved: spam_wordcloud.png")

print("\n" + "="*70)
print("5. DATA SPLITTING")
print("="*70)

X_train, X_test, y_train, y_test = train_test_split(df.Message, df.Spam, test_size=0.25, random_state=42)
print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

def evaluate_model(model, X_train, X_test, y_train, y_test):
    print("\nFitting model...")
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    pred_prob_train = model.predict_proba(X_train)[:, 1]
    pred_prob_test = model.predict_proba(X_test)[:, 1]

    roc_auc_train = roc_auc_score(y_train, pred_prob_train)
    roc_auc_test = roc_auc_score(y_test, pred_prob_test)
    print(f"\nTrain ROC AUC: {roc_auc_train:.4f}")
    print(f"Test ROC AUC: {roc_auc_test:.4f}")

    fpr_train, tpr_train, _ = roc_curve(y_train, pred_prob_train)
    fpr_test, tpr_test, _ = roc_curve(y_test, pred_prob_test)
    
    plt.figure(figsize=(8, 6))
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    plt.plot(fpr_train, tpr_train, label=f"Train ROC AUC: {roc_auc_train:.2f}")
    plt.plot(fpr_test, tpr_test, label=f"Test ROC AUC: {roc_auc_test:.2f}")
    plt.legend()
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.savefig('roc_curve.png', dpi=100, bbox_inches='tight')
    print("Saved: roc_curve.png")

    cm_train = confusion_matrix(y_train, y_pred_train)
    cm_test = confusion_matrix(y_test, y_pred_test)

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))

    print("\nConfusion Matrix:")
    sns.heatmap(cm_train, annot=True, xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'], 
                cmap="Oranges", fmt='d', ax=ax[0])
    ax[0].set_xlabel("Predicted Label")
    ax[0].set_ylabel("True Label")
    ax[0].set_title("Train Confusion Matrix")

    sns.heatmap(cm_test, annot=True, xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'], 
                cmap="Oranges", fmt='d', ax=ax[1])
    ax[1].set_xlabel("Predicted Label")
    ax[1].set_ylabel("True Label")
    ax[1].set_title("Test Confusion Matrix")

    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=100, bbox_inches='tight')
    print("Saved: confusion_matrix.png")

    cr_train = classification_report(y_train, y_pred_train, output_dict=True)
    cr_test = classification_report(y_test, y_pred_test, output_dict=True)
    
    print("\nTrain Classification Report:")
    print(pd.DataFrame(cr_train).T)
    print("\nTest Classification Report:")
    print(pd.DataFrame(cr_test).T)

    precision_train = cr_train['weighted avg']['precision']
    precision_test = cr_test['weighted avg']['precision']
    recall_train = cr_train['weighted avg']['recall']
    recall_test = cr_test['weighted avg']['recall']
    acc_train = accuracy_score(y_true=y_train, y_pred=y_pred_train)
    acc_test = accuracy_score(y_true=y_test, y_pred=y_pred_test)
    F1_train = cr_train['weighted avg']['f1-score']
    F1_test = cr_test['weighted avg']['f1-score']

    model_score = [precision_train, precision_test, recall_train, recall_test, acc_train, acc_test, roc_auc_train, roc_auc_test, F1_train, F1_test]
    return model_score

print("\n" + "="*70)
print("6. ML MODEL - MULTINOMIAL NAIVE BAYES")
print("="*70)

clf = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('nb', MultinomialNB())
])

model_scores = evaluate_model(clf, X_train, X_test, y_train, y_test)

def detect_spam(email_text):
    prediction = clf.predict([email_text])
    
    if prediction == 0:
        return "This is a Ham Email! ✓"
    else:
        return "This is a Spam Email! ✗"

print("\n" + "="*70)
print("7. EMAIL SPAM DETECTION SYSTEM - TESTING")
print("="*70)

test_emails = [
    'Free Tickets for IPL',
    'Hi, How are you doing?',
    'You have won a free prize. Click here to claim!',
    'Meeting scheduled for tomorrow at 2 PM',
    'Limited time offer - Get 50% off now!',
    'Can we connect for coffee this weekend?'
]

print("\nTesting the Spam Detection System:\n")
for email in test_emails:
    result = detect_spam(email)
    print(f"Email: '{email}'")
    print(f"Result: {result}\n")

print("="*70)
print("SPAM DETECTION SYSTEM COMPLETED SUCCESSFULLY!")
print("="*70)