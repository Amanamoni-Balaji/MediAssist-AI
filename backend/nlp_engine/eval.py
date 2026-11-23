import json
import joblib
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
try:
    from .preprocessor import TextPreprocessor
except ImportError:
    from preprocessor import TextPreprocessor


MODELS_DIR = Path(__file__).resolve().parent / "models"
DATA_PATH = Path(__file__).resolve().parent / "data" / "intents_dataset.json"

def evaluate_saved_model():
    model_path = MODELS_DIR / "intent_model.joblib"
    vec_path = MODELS_DIR / "tfidf_vectorizer.joblib"
    metrics_path = MODELS_DIR / "metrics.json"

    if not model_path.exists() or not vec_path.exists():
        print("Model or vectorizer artifact not found. Please run train.py first.")
        return

    classifier = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    preprocessor = TextPreprocessor()
    test_texts = []
    test_labels = []

    for intent in data['intents']:
        tag = intent['tag']
        for p in intent['patterns']:
            processed = preprocessor.preprocess(p)
            if processed:
                test_texts.append(processed)
                test_labels.append(tag)

    X_vec = vectorizer.transform(test_texts)
    y_pred = classifier.predict(X_vec)

    print("=== MODEL EVALUATION REPORT ===")
    print(classification_report(test_labels, y_pred, zero_division=0))
    print("Confusion Matrix:")
    print(confusion_matrix(test_labels, y_pred))

    if metrics_path.exists():
        with open(metrics_path, 'r', encoding='utf-8') as mf:
            metrics = json.load(mf)
            print("\nSaved Test Metrics:")
            print(f"Accuracy: {metrics.get('accuracy')}")
            print(f"Macro F1: {metrics.get('macro_f1')}")

if __name__ == "__main__":
    evaluate_saved_model()
