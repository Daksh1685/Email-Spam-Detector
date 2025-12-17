import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    f1_score, precision_score, recall_score, 
    confusion_matrix, classification_report, accuracy_score
)
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("EMAIL SPAM DETECTION - COMPREHENSIVE ANALYSIS REPORT")
print("="*80)

print("\n1. READING DATASET")
print("-"*80)
df = pd.read_csv("https://raw.githubusercontent.com/Apaulgithub/oibsip_taskno4/main/spam.csv", encoding='ISO-8859-1')
print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst 5 rows:")
print(df.head())

print("\n\n2. DATA PREPARATION")
print("-"*80)
df.rename(columns={"v1": "Category", "v2": "Message"}, inplace=True)
df.drop(columns={'Unnamed: 2','Unnamed: 3','Unnamed: 4'}, inplace=True, errors='ignore')
df['Spam'] = df['Category'].apply(lambda x: 1 if x == 'spam' else 0)
print(f"Data prepared successfully!")
print(f"Columns after preparation: {df.columns.tolist()}")
print(f"\nClass distribution:")
print(df['Category'].value_counts())
print(f"\nSpam labels distribution:")
print(df['Spam'].value_counts())

print("\n\n3. DESCRIPTIVE STATISTICS")
print("-"*80)
df['Message_Length'] = df['Message'].apply(len)
df['Word_Count'] = df['Message'].apply(lambda x: len(x.split()))
print("\nMessage Length Statistics:")
print(df['Message_Length'].describe())
print("\nWord Count Statistics:")
print(df['Word_Count'].describe())
print("\nMessage Statistics by Category:")
print(df.groupby('Category')[['Message_Length', 'Word_Count']].describe())

print("\n\n4. VISUAL ANALYSIS")
print("-"*80)
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

axes[0, 0].hist(df[df['Spam']==0]['Message_Length'], bins=50, label='Ham', alpha=0.7, color='green')
axes[0, 0].hist(df[df['Spam']==1]['Message_Length'], bins=50, label='Spam', alpha=0.7, color='red')
axes[0, 0].set_xlabel('Message Length')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].set_title('Message Length Distribution by Category')
axes[0, 0].legend()

axes[0, 1].hist(df[df['Spam']==0]['Word_Count'], bins=50, label='Ham', alpha=0.7, color='green')
axes[0, 1].hist(df[df['Spam']==1]['Word_Count'], bins=50, label='Spam', alpha=0.7, color='red')
axes[0, 1].set_xlabel('Word Count')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title('Word Count Distribution by Category')
axes[0, 1].legend()

df['Category'].value_counts().plot(kind='bar', ax=axes[1, 0], color=['green', 'red'])
axes[1, 0].set_title('Email Category Distribution')
axes[1, 0].set_ylabel('Count')
axes[1, 0].set_xticklabels(['Ham', 'Spam'], rotation=0)

df['Category'].value_counts().plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%', colors=['green', 'red'])
axes[1, 1].set_title('Email Category Percentage')
axes[1, 1].set_ylabel('')

plt.tight_layout()
plt.savefig('visual_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Visual analysis saved as 'visual_analysis.png'")
plt.close()

print("\n\n5. FEATURE EXTRACTION & VECTORIZATION")
print("-"*80)
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X = vectorizer.fit_transform(df['Message'])
y = df['Spam']
print(f"Feature matrix shape: {X.shape}")
print(f"Number of features extracted: {X.shape[1]}")

print("\n\n6. TRAIN-TEST SPLIT")
print("-"*80)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set size: {X_train.shape[0]}")
print(f"Testing set size: {X_test.shape[0]}")
print(f"Training spam percentage: {(y_train.sum()/len(y_train)*100):.2f}%")
print(f"Testing spam percentage: {(y_test.sum()/len(y_test)*100):.2f}%")

print("\n\n7. CORRELATION HEATMAP ANALYSIS")
print("-"*80)
print("Creating correlation matrix from top 15 features...")
top_features_indices = np.argsort(np.asarray(X_train.mean(axis=0)).ravel())[-15:]
X_train_dense = X_train[:, top_features_indices].toarray()
feature_names = [vectorizer.get_feature_names_out()[i] for i in top_features_indices]
correlation_matrix = pd.DataFrame(X_train_dense, columns=feature_names).corr()

plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', center=0, 
            square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('Correlation Heatmap of Top 20 Features', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Correlation heatmap saved as 'correlation_heatmap.png'")
plt.close()

print("\n\n8. STANDARD SCALING (for comparison)")
print("-"*80)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train.toarray())
X_test_scaled = scaler.transform(X_test.toarray())
print(f"Scaled training set shape: {X_train_scaled.shape}")
print(f"Scaled testing set shape: {X_test_scaled.shape}")
print(f"Mean of scaled training data: {X_train_scaled.mean():.6f}")
print(f"Std of scaled training data: {X_train_scaled.std():.6f}")

print("\n\n9. TRAINING MULTIPLE MODELS")
print("-"*80)

models = {
    'Multinomial Naive Bayes': MultinomialNB(),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
}

results = {}

for model_name, model in models.items():
    print(f"\nTraining {model_name}...")
    
    if model_name in ['Logistic Regression', 'Random Forest']:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    results[model_name] = {
        'model': model,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'predictions': y_pred
    }
    
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall: {recall:.4f}")
    print(f"  F1-Score: {f1:.4f}")

print("\n\n10. DETAILED METRICS - F1 SCORE, PRECISION, RECALL, SUPPORT")
print("-"*80)

for model_name, model_data in results.items():
    print(f"\n{'='*60}")
    print(f"{model_name}")
    print(f"{'='*60}")
    report = classification_report(y_test, model_data['predictions'], 
                                   target_names=['Ham', 'Spam'], 
                                   digits=4, output_dict=False)
    print(report)

print("\n\n11. MODEL COMPARISON")
print("-"*80)
comparison_df = pd.DataFrame({
    'Model': list(results.keys()),
    'Accuracy': [results[m]['accuracy'] for m in results.keys()],
    'Precision': [results[m]['precision'] for m in results.keys()],
    'Recall': [results[m]['recall'] for m in results.keys()],
    'F1-Score': [results[m]['f1'] for m in results.keys()]
})
print(comparison_df.to_string(index=False))

print("\n\n12. MODEL ACCURACY COMPARISON GRAPH")
print("-"*80)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

metrics_data = {
    'Accuracy': [results[m]['accuracy'] for m in results.keys()],
    'Precision': [results[m]['precision'] for m in results.keys()],
    'Recall': [results[m]['recall'] for m in results.keys()],
    'F1-Score': [results[m]['f1'] for m in results.keys()]
}

x_pos = np.arange(len(results))
width = 0.2

for i, metric in enumerate(['Accuracy', 'Precision']):
    axes[0].bar(x_pos + i*width, metrics_data[metric], width, label=metric)

axes[0].set_xlabel('Model', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Score', fontsize=12, fontweight='bold')
axes[0].set_title('Model Performance Comparison (Part 1)', fontsize=14, fontweight='bold')
axes[0].set_xticks(x_pos + width)
axes[0].set_xticklabels(results.keys(), rotation=45, ha='right')
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

for i, metric in enumerate(['Recall', 'F1-Score']):
    axes[1].bar(x_pos + i*width, metrics_data[metric], width, label=metric)

axes[1].set_xlabel('Model', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Score', fontsize=12, fontweight='bold')
axes[1].set_title('Model Performance Comparison (Part 2)', fontsize=14, fontweight='bold')
axes[1].set_xticks(x_pos + width)
axes[1].set_xticklabels(results.keys(), rotation=45, ha='right')
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Model comparison graph saved as 'model_comparison.png'")
plt.close()

print("\n\n13. CONFUSION MATRIX FOR EACH MODEL")
print("-"*80)
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes = axes.ravel()

for idx, (model_name, model_data) in enumerate(results.items()):
    cm = confusion_matrix(y_test, model_data['predictions'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], 
                xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'],
                cbar_kws={'label': 'Count'})
    axes[idx].set_title(f'{model_name}\nAccuracy: {model_data["accuracy"]:.4f}', 
                       fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('True Label', fontweight='bold')
    axes[idx].set_xlabel('Predicted Label', fontweight='bold')

plt.tight_layout()
plt.savefig('confusion_matrices.png', dpi=300, bbox_inches='tight')
print("✓ Confusion matrices saved as 'confusion_matrices.png'")
plt.close()

print("\n\n14. BEST MODEL DETAILED ANALYSIS")
print("-"*80)
best_model_name = max(results.keys(), key=lambda x: results[x]['f1'])
best_model_data = results[best_model_name]

print(f"\nBest Performing Model: {best_model_name}")
print(f"Accuracy: {best_model_data['accuracy']:.4f}")
print(f"Precision: {best_model_data['precision']:.4f}")
print(f"Recall: {best_model_data['recall']:.4f}")
print(f"F1-Score: {best_model_data['f1']:.4f}")

cm_best = confusion_matrix(y_test, best_model_data['predictions'])
print(f"\nConfusion Matrix:")
print(f"True Negatives (TN): {cm_best[0, 0]}")
print(f"False Positives (FP): {cm_best[0, 1]}")
print(f"False Negatives (FN): {cm_best[1, 0]}")
print(f"True Positives (TP): {cm_best[1, 1]}")

print(f"\nDetailed Classification Report:")
print(classification_report(y_test, best_model_data['predictions'], 
                          target_names=['Ham', 'Spam']))

print("\n\n15. SAMPLE PREDICTIONS")
print("-"*80)
sample_emails = [
    "Congratulations! You've won a free iPhone. Click here to claim your prize.",
    "Hi, can we schedule a meeting for tomorrow at 2 PM?",
    "You have been selected for a special offer. Click now to redeem!",
    "The project report is ready for review. Please check the attachment."
]

print("\nTesting with sample emails:")
for email in sample_emails:
    email_vec = vectorizer.transform([email])
    
    if best_model_name in ['Logistic Regression', 'Linear SVM', 'Random Forest']:
        email_scaled = scaler.transform(email_vec.toarray())
        prediction = best_model_data['model'].predict(email_scaled)[0]
    else:
        prediction = best_model_data['model'].predict(email_vec)[0]
    
    result = "SPAM" if prediction == 1 else "HAM"
    print(f"\n  Email: {email[:60]}...")
    print(f"  Prediction: {result}")

print("\n\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print("\nGenerated files:")
print("  ✓ visual_analysis.png")
print("  ✓ correlation_heatmap.png")
print("  ✓ model_comparison.png")
print("  ✓ confusion_matrices.png")
print("="*80)
