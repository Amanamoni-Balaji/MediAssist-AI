import os
import joblib
from pathlib import Path
from .preprocessor import TextPreprocessor

MODELS_DIR = Path(__file__).resolve().parent / "models"

class IntentClassifier:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.model = None
        self.vectorizer = None
        self.classes = []
        self.load_model()

    def load_model(self):
        model_path = MODELS_DIR / "intent_model.joblib"
        vec_path = MODELS_DIR / "tfidf_vectorizer.joblib"
        classes_path = MODELS_DIR / "classes.joblib"

        if not model_path.exists() or not vec_path.exists():
            # If model does not exist yet, import and train
            from .train import train_intent_model
            train_intent_model()

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vec_path)
        if classes_path.exists():
            self.classes = joblib.load(classes_path)
        else:
            self.classes = list(self.model.classes_)

    def predict(self, text: str) -> tuple[str, float, dict]:
        """
        Classifies intent of input text.
        Returns:
            (predicted_intent, confidence_score, all_class_probabilities)
        """
        processed = self.preprocessor.preprocess(text)
        if not processed:
            return "general_faq", 0.0, {}

        vec = self.vectorizer.transform([processed])
        
        # Predict probability distribution
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(vec)[0]
            max_idx = probs.argmax()
            predicted_intent = self.model.classes_[max_idx]
            confidence = float(probs[max_idx])
            prob_dict = {cls_name: round(float(p), 4) for cls_name, p in zip(self.model.classes_, probs)}
        else:
            predicted_intent = self.model.predict(vec)[0]
            confidence = 0.85
            prob_dict = {predicted_intent: 0.85}

        # Apply confidence thresholding: if confidence is too low, label as general inquiry
        if confidence < 0.25:
            predicted_intent = "general_faq"

        return predicted_intent, round(confidence, 4), prob_dict

