import re

# High priority emergency patterns
EMERGENCY_PATTERNS = [
    r'\b(crushing|severe|radiating|sharp)\s+chest\s+pain\b',
    r'\bchest\s+(pain|pressure|tightness|squeezing)\b.*\b(arm|jaw|neck|back|shoulder)\b',
    r'\b(cannot|can\'t)\s+breathe\b',
    r'\b(severe|acute)\s+shortness\s+of\s+breath\b',
    r'\b(blue|bluish)\s+(lips|fingers|skin)\b',
    r'\b(face\s+(?:is\s+)?droop\w*|slurred\s+speech|arm\s+(?:weakness|numbness)|(?:cannot|can\'?t)\s+move\s+(?:my\s+)?arm|stroke)\b',
    r'\b(sudden\s+paralysis|sudden\s+numbness\s+on\s+one\s+side)\b',
    r'\bcoughing\s+up\s+blood\b',
    r'\bvomiting\s+blood\b',
    r'\b(suicid|kill\s+myself|end\s+my\s+life|want\s+to\s+die)\b',
    r'\b(anaphylaxis|throat\s+closing|throat\s+swelling)\b',
    r'\b(thunderclap|explosive)\s+headache\b',
    r'\bunconscious|loss\s+of\s+consciousness|passed\s+out\b',
    r'\bsevere\s+allergic\s+reaction\b',
    r'\bprofuse\s+bleeding\b',
    r'\bheart\s+attack\b',
    r'\bstiff\s+neck\b.*\b(high\s+fever|confusion)\b'
]

EMERGENCY_DISCLAIMER_MESSAGE = (
    "🚨 CRITICAL MEDICAL ADVISORY: The symptoms you described may represent a life-threatening medical emergency. "
    "DO NOT wait for an online response or attempt self-treatment.\n\n"
    "• In the United States/Canada, call 911 immediately.\n"
    "• In the United Kingdom, call 999.\n"
    "• In Europe, call 112.\n"
    "• If in immediate emotional distress or experiencing suicidal thoughts, call or text 988 (Lifeline) or go to the nearest emergency department.\n\n"
    "Please seek emergency professional medical intervention right now."
)

class EmergencyDetector:
    def __init__(self):
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in EMERGENCY_PATTERNS]

    def check(self, text: str) -> tuple[bool, str | None]:
        text_lower = text.lower()
        for pattern in self.compiled_patterns:
            if pattern.search(text_lower):
                return True, EMERGENCY_DISCLAIMER_MESSAGE
        return False, None

