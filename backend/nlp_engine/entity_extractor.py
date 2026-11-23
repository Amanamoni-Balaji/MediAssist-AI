import json
import os
import re
from pathlib import Path
from .preprocessor import TextPreprocessor

DICTIONARY_PATH = Path(__file__).resolve().parent / "data" / "medical_dictionary.json"

class MedicalEntityExtractor:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.symptoms = []
        self.conditions = []
        self.body_parts = []
        self.severity_markers = []
        self.load_dictionary()

    def load_dictionary(self):
        if os.path.exists(DICTIONARY_PATH):
            with open(DICTIONARY_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.symptoms = [s.lower() for s in data.get('symptoms', [])]
                self.conditions = [c.lower() for c in data.get('conditions', [])]
                self.body_parts = [b.lower() for b in data.get('body_parts', [])]
                self.severity_markers = [sm.lower() for sm in data.get('severity_markers', [])]

    def extract(self, text: str) -> dict:
        text_lower = text.lower()
        cleaned_text = self.preprocessor.clean_text(text)
        tokens = self.preprocessor.tokenize(text)
        lemmatized_tokens = self.preprocessor.lemmatize_tokens(tokens)
        lemmatized_str = " ".join(lemmatized_tokens)

        found_symptoms = set()
        found_conditions = set()
        found_body_parts = set()
        found_severity = set()

        # Check multi-word and single-word symptoms
        for symptom in sorted(self.symptoms, key=len, reverse=True):
            if re.search(r'\b' + re.escape(symptom) + r'\b', text_lower) or \
               re.search(r'\b' + re.escape(symptom) + r'\b', lemmatized_str):
                found_symptoms.add(symptom)

        # Check conditions
        for condition in sorted(self.conditions, key=len, reverse=True):
            if re.search(r'\b' + re.escape(condition) + r'\b', text_lower) or \
               re.search(r'\b' + re.escape(condition) + r'\b', lemmatized_str):
                found_conditions.add(condition)

        # Check body parts
        for bp in self.body_parts:
            if re.search(r'\b' + re.escape(bp) + r'\b', text_lower) or \
               re.search(r'\b' + re.escape(bp) + r'\b', lemmatized_str):
                found_body_parts.add(bp)

        # Check severity
        for sm in self.severity_markers:
            if re.search(r'\b' + re.escape(sm) + r'\b', text_lower):
                found_severity.add(sm)

        # Extract duration patterns (e.g., "for 3 days", "since yesterday", "2 weeks")
        duration_match = re.findall(r'\b(\d+\s*(?:days?|weeks?|months?|hours?)|since\s+\w+|for\s+\w+)\b', text_lower)

        return {
            "symptoms": sorted(list(found_symptoms)),
            "conditions": sorted(list(found_conditions)),
            "body_parts": sorted(list(found_body_parts)),
            "severity": sorted(list(found_severity)),
            "durations": duration_match
        }

