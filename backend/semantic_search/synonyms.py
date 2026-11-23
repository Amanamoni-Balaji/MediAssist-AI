import re

# Comprehensive synonym and semantic concept mapping
# Maps colloquial user phrases and symptoms to clinical concepts and expanded keywords
SEMANTIC_CONCEPT_MAP = {
    # Skin & Dermatology
    "hyperhidrosis": [
        "sweat", "sweating", "sweaty", "perspiration", "wet hands", "sweaty palms", "sweaty feet",
        "sweat in hands", "underarms sweat", "sweating too much", "hands wet", "feet sweat",
        "excessive sweating", "diaphoresis", "palmar hyperhidrosis", "plantar hyperhidrosis",
        "axillary hyperhidrosis", "sweat glands", "clammy hands", "dripping sweat"
    ],
    "acne": [
        "acne", "pimple", "pimples", "zits", "breakout", "blackheads", "whiteheads",
        "cystic acne", "facial spots", "comedones", "oily skin breakout", "blemishes"
    ],
    "eczema": [
        "eczema", "atopic dermatitis", "itchy skin", "skin inflammation", "dry red patches",
        "skin itching", "itchy rash", "skin flaking", "dermatitis flare"
    ],
    "psoriasis": [
        "psoriasis", "silvery scales", "scaly skin patches", "plaque psoriasis",
        "red scaly plaques", "elbow scales", "knee plaques", "scalp psoriasis"
    ],
    "fungal_infection": [
        "fungal infection", "ringworm", "athlete's foot", "tinea", "jock itch",
        "fungus on skin", "fungal rash", "peeling foot skin", "itchy groin"
    ],
    "hair_fall": [
        "hair fall", "hair loss", "hair falling", "losing hair", "hair thinning",
        "alopecia", "receding hairline", "bald patches", "telogen effluvium", "shedding hair"
    ],
    "dry_skin": [
        "dry skin", "xerosis", "rough skin", "flaky skin", "skin peeling", "ashy skin"
    ],

    # General Medicine & Symptoms
    "fever": [
        "fever", "pyrexia", "high temperature", "feverish", "chills", "feeling hot and cold",
        "body temperature high", "shivering fever", "fevr"
    ],
    "headache": [
        "headache", "head pain", "head is paining", "throbbing head", "temple pain",
        "tension headache", "forehead pressure", "hedache", "head ache"
    ],
    "migraine": [
        "migraine", "severe one-sided headache", "migraine aura", "throbbing headache",
        "light sensitivity headache", "photophobia", "nausea with headache", "migrain"
    ],
    "body_pain": [
        "body pain", "body ache", "muscle pain", "myalgia", "whole body hurting",
        "generalized aches", "sore muscles", "body fatigue"
    ],
    "fatigue": [
        "fatigue", "tiredness", "exhaustion", "feeling weak from morning", "low energy",
        "chronic fatigue", "lethargy", "no energy", "sluggishness", "worn out"
    ],
    "dizziness": [
        "dizziness", "dizzy", "lightheaded", "lightheadedness", "room spinning",
        "vertigo", "feeling faint", "unsteady", "loss of balance"
    ],
    "vomiting_nausea": [
        "vomiting", "nausea", "throwing up", "feeling sick", "upset stomach vomiting",
        "queasy", "puking", "retch", "emesis"
    ],
    "diarrhea": [
        "diarrhea", "loose stools", "watery stools", "frequent bathroom trips",
        "upset bowel", "gastroenteritis", "stomach flu"
    ],

    # Respiratory Health
    "common_cold": [
        "cold", "common cold", "runny nose", "sneezing", "stuffy nose", "nasal congestion",
        "rhinovirus", "head cold", "blocked nose"
    ],
    "cough": [
        "cough", "coughing", "dry cough", "wet cough", "hacking cough", "persistent cough",
        "cough with phlegm", "throat clearing", "chest cough"
    ],
    "asthma": [
        "asthma", "wheezing", "asthma attack", "tight chest", "airway constriction",
        "inhaler", "bronchospasm", "getting breathing problem", "whistling breath"
    ],
    "bronchitis": [
        "bronchitis", "chest congestion", "bronchial inflammation", "deep chest cough",
        "yellow green mucus cough", "acute bronchitis"
    ],
    "sore_throat": [
        "sore throat", "throat pain", "scratchy throat", "pharyngitis", "pain swallowing",
        "irritated throat", "raw throat"
    ],
    "sinusitis": [
        "sinusitis", "sinus infection", "sinus pressure", "facial pressure",
        "blocked sinuses", "pain behind eyes and nose", "nasal sinus pain"
    ],

    # Cardiovascular Health
    "hypertension": [
        "hypertension", "high blood pressure", "high bp", "elevated bp", "bp high",
        "systolic pressure", "diastolic pressure", "hypertensive", "blood pressure reading"
    ],
    "low_blood_pressure": [
        "low blood pressure", "low bp", "hypotension", "dizzy when standing",
        "orthostatic hypotension", "fainting bp"
    ],
    "heart_disease": [
        "heart disease", "cardiovascular disease", "coronary artery disease", "atherosclerosis",
        "artery plaque", "heart health", "cardiac wellness"
    ],
    "cholesterol": [
        "cholesterol", "high cholesterol", "ldl", "hdl", "triglycerides", "hyperlipidemia",
        "blood lipid profile", "artery clogging fat"
    ],
    "palpitations": [
        "palpitations", "racing heart", "heart skipping a beat", "fluttering heart",
        "fast pulse", "irregular heartbeat", "tachycardia"
    ],

    # Endocrine & Metabolic Health
    "diabetes": [
        "diabetes", "type 2 diabetes", "type 1 diabetes", "high blood sugar", "insulin resistance",
        "hyperglycemia", "diabetic", "frequent urination thirsty", "hba1c", "blood glucose"
    ],
    "thyroid": [
        "thyroid", "hypothyroidism", "hyperthyroidism", "underactive thyroid", "overactive thyroid",
        "tsh", "goiter", "thyroid nodules", "sluggish metabolism thyroid"
    ],
    "pcos": [
        "pcos", "polycystic ovary syndrome", "irregular periods", "facial hair women",
        "polycystic ovaries", "hormonal imbalance women", "acne and irregular cycles"
    ],
    "obesity": [
        "obesity", "overweight", "excess weight", "high bmi", "weight gain",
        "weight management", "visceral fat", "morbid obesity"
    ],

    # Mental Health & Sleep
    "insomnia": [
        "insomnia", "cannot sleep", "can't sleep", "trouble sleeping", "sleeplessness",
        "sleep disorder", "waking up at night", "not getting sleep", "poor sleep",
        "sleep hygiene", "irregular sleep schedule", "broken sleep", "blue light",
        "hours of sleep", "bedroom temperature", "sleep quality"
    ],
    "anxiety": [
        "anxiety", "generalized anxiety", "panic attack", "constant worry", "nervousness",
        "feeling on edge", "anxious thoughts", "heart racing worry", "breathing techniques"
    ],
    "stress": [
        "stress", "chronic stress", "burnout", "overwhelmed", "mental tension",
        "high cortisol", "work stress", "emotional strain", "manage chronic stress"
    ],
    "depression": [
        "depression", "clinical depression", "feeling hopeless", "low mood", "loss of interest",
        "sadness", "major depressive disorder", "depressive symptoms"
    ],

    # Digestive Health
    "gastritis": [
        "gastritis", "stomach inflammation", "stomach burning after food", "burning in stomach",
        "acidic stomach", "epigastric burning", "indigestion burning", "stomach burns after eating"
    ],
    "acid_reflux": [
        "acid reflux", "gerd", "heartburn", "acid regurgitation", "sour taste in mouth",
        "chest burning after eating", "reflux disease", "stomach burning after food",
        "stomach burns after eating", "lying down after eating"
    ],
    "stomach_pain": [
        "stomach pain", "abdominal pain", "my stomach hurts", "belly ache", "tummy pain",
        "stomach cramps", "cramps in belly", "gut pain", "stomac ache", "nsaids on empty stomach"
    ],
    "constipation": [
        "constipation", "hard stools", "straining bowel", "infrequent bowel movement",
        "irregular bowels", "bowel blockage"
    ],
    "ibs": [
        "ibs", "irritable bowel syndrome", "spastic colon", "cramping with diarrhea and constipation",
        "bloating and gas pain", "sensitive bowel"
    ],
    "liver_health": [
        "liver health", "fatty liver", "hepatic steatosis", "elevated liver enzymes",
        "liver detox", "nonalcoholic fatty liver", "non-alcoholic fatty liver"
    ],
    "kidney_health": [
        "kidney health", "renal function", "kidney stones", "creatinine",
        "filtering waste kidneys", "nephrology"
    ],

    # Nutrition & Lifestyle
    "hemoglobin": [
        "hemoglobin", "haemoglobin", "low hb", "boost hemoglobin", "raise hemoglobin",
        "iron deficiency", "anemia", "red blood cells", "ferritin", "iron rich foods",
        "heamoglobin", "tea or coffee with meals"
    ],
    "dietary_protein": [
        "protein", "dietary protein", "protein requirements", "protein per day",
        "plant protein", "lean protein", "protein for muscle recovery", "muscle tissue repair"
    ],
    "balanced_diet": [
        "balanced diet", "healthy eating", "nutrition", "macro nutrients", "mediterranean diet",
        "dash diet", "eating healthy plate", "fiber intake", "healthy lifestyle", "maintain a healthy lifestyle",
        "ultra-processed foods", "dietary fiber", "vitamin d deficiency"
    ],
    "hydration": [
        "hydration", "drinking water", "dehydration", "electrolyte balance",
        "glasses of water per day", "fluid intake", "dark urine and dry mouth"
    ],
    "exercise": [
        "exercise", "physical activity", "daily walking", "aerobic exercise",
        "cardio workouts", "strength training", "yoga flexibility", "aerobic cardio",
        "30 minutes of daily walking", "moderate aerobic exercise"
    ],

    # Women's & Men's Health
    "menstrual_health": [
        "menstrual health", "menstrual cramps", "period pain", "dysmenorrhea",
        "heavy periods", "irregular cycle", "pms", "premenstrual syndrome"
    ],
    "pregnancy_education": [
        "pregnancy education", "prenatal care", "morning sickness", "fetal development",
        "healthy pregnancy tips", "gestational health"
    ],
    "menopause": [
        "menopause", "hot flashes", "night sweats", "perimenopause",
        "hormone transition", "estrogen decline"
    ],
    "prostate_health": [
        "prostate health", "bph", "enlarged prostate", "frequent night urination men",
        "prostate awareness"
    ],

    # Medical Education
    "virus_vs_bacteria": [
        "difference between virus and bacteria", "viruses and bacteria", "compare virus and bacteria",
        "antibiotics on viruses", "bacterial vs viral infection", "pathogen differences"
    ],
    "first_aid": [
        "first aid", "emergency first aid", "burn first aid", "cut first aid",
        "sprain first aid", "choking first aid", "nosebleed first aid", "thermal skin burn",
        "ice or butter on a fresh burn", "rice protocol", "nosebleed", "lean forward during a nosebleed",
        "heimlich maneuver", "bleeding laceration cut", "direct pressure"
    ]
}


class SynonymExpander:
    """
    Expands user queries with clinical synonyms and related terminology.
    Enables semantic matching even when users use 100% informal or colloquial vocabulary.
    """
    def __init__(self):
        # Invert the mapping: word/phrase -> canonical concept
        self.phrase_to_concept = {}
        for concept, phrases in SEMANTIC_CONCEPT_MAP.items():
            for phrase in phrases:
                self.phrase_to_concept[phrase.lower()] = concept

        # Sort phrases by length descending to match longest multi-word phrases first
        self.sorted_phrases = sorted(self.phrase_to_concept.keys(), key=len, reverse=True)

    def identify_concepts(self, text: str) -> list[str]:
        """Finds all clinical concepts present in the text."""
        text_lower = text.lower()
        matched_concepts = []
        for phrase in self.sorted_phrases:
            pattern = r'\b' + re.escape(phrase) + r'\b'
            if re.search(pattern, text_lower):
                concept = self.phrase_to_concept[phrase]
                if concept not in matched_concepts:
                    matched_concepts.append(concept)
        return matched_concepts

    def expand_query(self, query: str) -> str:
        """
        Takes a raw user query and returns an enriched semantic query string
        containing both the original text and its clinical synonym keywords.
        """
        concepts = self.identify_concepts(query)
        if not concepts:
            return query

        expanded_terms = []
        for concept in concepts:
            # Add top canonical terms for this concept
            top_terms = SEMANTIC_CONCEPT_MAP.get(concept, [])[:6]
            expanded_terms.extend(top_terms)

        # De-duplicate while preserving order
        unique_terms = []
        for t in expanded_terms:
            if t not in unique_terms and t not in query.lower():
                unique_terms.append(t)

        if unique_terms:
            enriched = f"{query} {' '.join(unique_terms[:8])}"
            return enriched
        return query
