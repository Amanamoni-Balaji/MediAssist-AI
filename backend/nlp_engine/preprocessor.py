import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Contraction mapping
CONTRACTIONS = {
    "can't": "cannot",
    "won't": "will not",
    "n't": " not",
    "'re": " are",
    "'s": " is",
    "'d": " would",
    "'ll": " will",
    "'t": " not",
    "'ve": " have",
    "'m": " am",
    "i'm": "i am",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not"
}

# Common typos and phonetic misspellings in medical queries and everyday English
TYPO_CORRECTIONS = {
    "diabeetes": "diabetes",
    "diabtes": "diabetes",
    "diabetis": "diabetes",
    "diabetic": "diabetes",
    "hypertenshion": "hypertension",
    "hypertention": "hypertension",
    "hyprtension": "hypertension",
    "hedache": "headache",
    "head ache": "headache",
    "headach": "headache",
    "fevr": "fever",
    "feever": "fever",
    "fevour": "fever",
    "stomache": "stomach",
    "stomac": "stomach",
    "stomech": "stomach",
    "insomniaa": "insomnia",
    "insomna": "insomnia",
    "sleeep": "sleep",
    "sleping": "sleeping",
    "slept": "sleep",
    "heamoglobin": "hemoglobin",
    "haemoglobin": "hemoglobin",
    "heamoglobin": "hemoglobin",
    "hemogloblin": "hemoglobin",
    "thyrod": "thyroid",
    "tyroid": "thyroid",
    "throid": "thyroid",
    "fatig": "fatigue",
    "fatige": "fatigue",
    "tierd": "tired",
    "tierdness": "tiredness",
    "exhastion": "exhaustion",
    "nauseous": "nausea",
    "nausia": "nausea",
    "vomitng": "vomiting",
    "arthiritis": "arthritis",
    "arthrits": "arthritis",
    "anxity": "anxiety",
    "anxietie": "anxiety",
    "depresion": "depression",
    "protien": "protein",
    "protiens": "protein",
    "paracetemol": "paracetamol",
    "paracetmol": "paracetamol",
    "breathin": "breathing",
    "breathlessness": "shortness of breath",
    "bactria": "bacteria",
    "viruss": "virus",
    "vires": "virus",
    "dizzy": "dizziness",
    "dizzyness": "dizziness",
    "migrain": "migraine",
    "migrane": "migraine",
    "gastritus": "gastritis",
    "infecton": "infection",
    "medisin": "medicine",
    "doc": "doctor"
}

# Colloquial and natural phrase normalization
COLLOQUIAL_PATTERNS = [
    # Sleep difficulties
    (r"\b(didn't|did not|couldn't|could not|cannot|can't|not)\s+(get|getting|have|having|fall)\s+sleep\b", "insomnia sleep difficulty"),
    (r"\b(unable|trouble|problem|hard)\s+(to\s+)?sleep\b", "insomnia sleep difficulty"),
    (r"\b(can't|cannot)\s+sleep\s+(at\s+night)?\b", "insomnia sleep difficulty"),
    (r"\b(not\s+getting|poor|bad)\s+sleep\b", "insomnia sleep difficulty"),
    (r"\b(sleeplessness|sleepless|waking up at night|awake all night)\b", "insomnia sleep difficulty"),

    # Stomach / abdominal pain
    (r"\b(stomach|belly|tummy|gut|abdomen)\s+(hurts?|aching|aches?|pain|cramp|cramps|upset)\b", "abdominal pain stomach ache"),
    (r"\b(pain|cramps?)\s+in\s+(my\s+)?(stomach|belly|tummy|abdomen|gut)\b", "abdominal pain stomach ache"),
    (r"\bacidity|burning in stomach|acid in stomach\b", "acid reflux gastritis"),

    # Hemoglobin & Iron
    (r"\b(how\s+to\s+)?(increase|raise|boost|improve|elevate)\s+(hemoglobin|haemoglobin|hb|iron|blood level)\b", "increase hemoglobin iron deficiency anemia"),
    (r"\b(low\s+)(hemoglobin|haemoglobin|hb|iron in blood)\b", "iron deficiency anemia hemoglobin"),

    # Common greetings and friendly questions
    (r"\bhow\s+are\s+you(\s+doing)?\b", "how are you general conversation"),
    (r"\bhow('s| is)\s+it\s+going\b", "how are you general conversation"),
    (r"\bwhat('s| is)\s+up\b", "how are you general conversation"),
    (r"\bwhat\s+are\s+you\s+doing\b", "what are you doing general conversation"),
    (r"\btell\s+me\s+something\s+interesting\b", "tell me something interesting general conversation"),

    # Chatbot identity and capabilities
    (r"\bwho\s+are\s+you\b", "who are you chatbot identity"),
    (r"\bwhat\s+(can\s+you|are\s+you\s+able\s+to)\s+do\b", "what can you do chatbot capabilities"),
    (r"\bcan\s+you\s+help\s+me\b", "can you help me chatbot capabilities"),
    (r"\bwhat\s+is\s+your\s+name\b", "who are you chatbot identity"),

    # Clarification and simplification
    (r"\b(explain|say\s+it|tell\s+me)\s+(it\s+)?in\s+simple\s+(words|terms|english)\b", "explain in simple words clarification"),
    (r"\b(explain\s+again|can\s+you\s+explain\s+again|i\s+do\s+not\s+understand|i\s+didn't\s+understand)\b", "explain again clarification"),
    (r"\b(give\s+me\s+more\s+information|tell\s+me\s+more|elaborate|more\s+details)\b", "give more information clarification"),
    (r"\b(make\s+it\s+simpler|simplify\s+this|in\s+plain\s+words)\b", "explain in simple words clarification"),

    # High blood pressure and sugar
    (r"\bhigh\s+bp\b", "hypertension high blood pressure"),
    (r"\b(sugar|diabetes)\s+(level|high)\b", "type 2 diabetes blood sugar"),

    # Viruses vs bacteria
    (r"\b(difference\s+between|compare)\s+(virus(es)?\s+and\s+bacteria|bacteria\s+and\s+virus(es)?)\b", "difference between viruses and bacteria"),
]

# Negations and critical medical terms and interrogative words to preserve
PRESERVED_WORDS = {
    "no", "not", "none", "without", "never", "high", "low", "pain", "more", "less",
    "what", "how", "why", "when", "where", "who", "can", "could", "should", "is", "are",
    "do", "does", "did", "to", "for", "of", "in", "with", "between", "difference",
    "you", "your", "i", "me", "my", "we", "us", "am", "doing", "help", "hello", "hi",
    "hey", "tell", "explain", "understand", "again", "simple", "words", "burn", "cut",
    "cold", "flu", "sleep", "stomach", "ache", "iron", "blood", "care", "relief"
}


class TextPreprocessor:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english')) - PRESERVED_WORDS
        except Exception:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english')) - PRESERVED_WORDS
            
        try:
            self.lemmatizer = WordNetLemmatizer()
        except Exception:
            nltk.download('wordnet')
            self.lemmatizer = WordNetLemmatizer()

    def expand_contractions(self, text: str) -> str:
        text = text.lower()
        for contraction, replacement in CONTRACTIONS.items():
            text = text.replace(contraction, replacement)
        return text

    def correct_typos(self, text: str) -> str:
        """Replace common misspelled medical and conversational words."""
        words = text.split()
        corrected_words = []
        for word in words:
            # Strip punctuation attached to word
            clean_w = word.strip(string.punctuation).lower()
            if clean_w in TYPO_CORRECTIONS:
                corrected_words.append(TYPO_CORRECTIONS[clean_w])
            else:
                corrected_words.append(word)
        return " ".join(corrected_words)

    def normalize_colloquialisms(self, text: str) -> str:
        """Map common everyday phrases and idioms to canonical clinical / conversational queries."""
        normalized = text.lower()
        for pattern, replacement in COLLOQUIAL_PATTERNS:
            if re.search(pattern, normalized, re.IGNORECASE):
                normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        return normalized

    def clean_text(self, text: str) -> str:
        """Lowercase, expand contractions, correct typos, normalize idioms, remove punctuation."""
        if not text:
            return ""
        text = self.expand_contractions(text)
        text = self.correct_typos(text)
        text = self.normalize_colloquialisms(text)
        # Keep alphanumeric, spaces, and hyphens (e.g. iron-deficiency)
        text = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def tokenize(self, text: str) -> list[str]:
        """Tokenize cleaned string."""
        cleaned = self.clean_text(text)
        try:
            tokens = word_tokenize(cleaned)
        except Exception:
            tokens = cleaned.split()
        return tokens

    def lemmatize_tokens(self, tokens: list[str]) -> list[str]:
        """Lemmatize tokens into base forms."""
        return [self.lemmatizer.lemmatize(token) for token in tokens]

    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        """Filter out stopwords while keeping medical context words."""
        return [t for t in tokens if t not in self.stop_words and len(t) > 1]

    def preprocess(self, text: str, remove_stop: bool = True) -> str:
        """Complete pipeline: clean -> tokenize -> filter stopwords -> lemmatize -> join."""
        tokens = self.tokenize(text)
        if remove_stop:
            tokens = self.remove_stopwords(tokens)
        lemmatized = self.lemmatize_tokens(tokens)
        return " ".join(lemmatized)
