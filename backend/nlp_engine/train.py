import json
import os
import joblib
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support

try:
    from .preprocessor import TextPreprocessor
except ImportError:
    from preprocessor import TextPreprocessor


DATA_PATH = Path(__file__).resolve().parent / "data" / "intents_dataset.json"
MODELS_DIR = Path(__file__).resolve().parent / "models"

def train_intent_model():
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    preprocessor = TextPreprocessor()

    texts = []
    labels = []

    for intent in data['intents']:
        tag = intent['tag']
        for pattern in intent['patterns']:
            processed = preprocessor.preprocess(pattern)
            if processed:
                texts.append(processed)
                labels.append(tag)

    print(f"Loaded {len(texts)} training samples across {len(set(labels))} intent classes.")

    # Train / Test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.15, random_state=42, stratify=labels
    )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        sublinear_tf=True,
        min_df=1
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    base_svm = LinearSVC(C=1.0, random_state=42, dual='auto')
    classifier = CalibratedClassifierCV(estimator=base_svm, cv=3)
    classifier.fit(X_train_vec, y_train)

    y_pred = classifier.predict(X_test_vec)

    # Compute evaluation metrics
    acc = float(accuracy_score(y_test, y_pred))
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_test, y_pred, average='macro', zero_division=0)
    p_weight, r_weight, f1_weight, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
    conf_mat = confusion_matrix(y_test, y_pred).tolist()
    labels_list = sorted(list(set(labels)))

    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    metrics = {
        "accuracy": round(acc, 4),
        "macro_precision": round(float(p_macro), 4),
        "macro_recall": round(float(r_macro), 4),
        "macro_f1": round(float(f1_macro), 4),
        "weighted_precision": round(float(p_weight), 4),
        "weighted_recall": round(float(r_weight), 4),
        "weighted_f1": round(float(f1_weight), 4),
        "test_sample_count": len(y_test),
        "train_sample_count": len(y_train),
        "intent_classes": labels_list,
        "confusion_matrix": conf_mat,
        "classification_report": report
    }

    print("\n--- MODEL EVALUATION SUMMARY ---")
    print(f"Accuracy: {metrics['accuracy'] * 100:.2f}%")
    print(f"Macro F1-Score: {metrics['macro_f1']:.4f}")
    print(f"Macro Precision: {metrics['macro_precision']:.4f}")
    print(f"Macro Recall: {metrics['macro_recall']:.4f}")

    # Save artifacts
    joblib.dump(classifier, MODELS_DIR / "intent_model.joblib")
    joblib.dump(vectorizer, MODELS_DIR / "tfidf_vectorizer.joblib")
    joblib.dump(labels_list, MODELS_DIR / "classes.joblib")

    with open(MODELS_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Artifacts successfully saved to {MODELS_DIR}")
    return metrics

if __name__ == "__main__":
    train_intent_model()
