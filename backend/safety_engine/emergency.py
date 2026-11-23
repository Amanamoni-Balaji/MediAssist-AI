import re

# High-precision emergency patterns covering genuine life-threatening emergencies
EMERGENCY_PATTERNS = [
    # Acute coronary syndromes / Myocardial infarction
    r'\b(?:severe|crushing|acute|radiating|sharp)\s+chest\s+pain\b',
    r'\bchest\s+(?:pain|pressure|tightness|squeezing)\b.*\b(?:arm|jaw|neck|back|shoulder)\b',
    r'\bchest\s+is\s+hurting\b.*\b(?:cannot|can\'?t)\s+breathe\b',
    r'\b(?:heart\s+attack|cardiac\s+arrest)\b',

    # Severe acute respiratory distress
    r'\b(?:cannot|can\'?t)\s+breathe\s+(?:at\s+all|properly)\b',
    r'\b(?:severe|acute)\s+shortness\s+of\s+breath\b',
    r'\b(?:lips|fingers|skin)\s+(?:are\s+)?turning\s+blue\b',
    r'\bblue\s+(?:lips|fingers|skin)\b',
    r'\basphyxiation|choking\s+and\s+(?:cannot|can\'?t)\s+inhale\b',

    # Acute stroke / Cerebrovascular accident
    r'\b(?:face\s+(?:is\s+)?droop\w*|slurred\s+speech|arm\s+(?:weakness|numbness)|(?:cannot|can\'?t)\s+move\s+(?:my\s+)?arm|stroke)\b',
    r'\bsudden\s+(?:paralysis|facial\s+paralysis|loss\s+of\s+speech|numbness\s+on\s+one\s+side)\b',

    # Anaphylaxis / Severe airway edema
    r'\b(?:anaphylaxis|anaphylactic\s+shock|throat\s+(?:is\s+)?(?:closing|swelling\s+shut))\b',
    r'\bsevere\s+allergic\s+reaction\b.*\bthroat\b',

    # Hemorrhage / Acute internal bleeding
    r'\b(?:coughing|vomiting)\s+up\s+blood\b',
    r'\bprofuse\s+(?:arterial\s+)?bleeding\b',
    r'\bdeep\s+cut\s+bleeding\s+continuously\b',

    # Neurological emergencies
    r'\b(?:thunderclap|explosive)\s+headache\b',
    r'\bunresponsive|loss\s+of\s+consciousness|passed\s+out\b.*\bwon\'?t\s+wake\b',
    r'\bprolonged\s+seizure\b',

    # Acute psychiatric crisis / Suicidal ideation
    r'\b(?:suicid\w*|kill\s+myself|end\s+my\s+life|want\s+to\s+die|harm\s+myself)\b',

    # Severe acute surgical abdomen
    r'\bsevere\s+acute\s+abdominal\s+pain\b.*\bvomiting\s+blood\b',
]

EMERGENCY_RESPONSE_MESSAGE = (
    "🚨 **CRITICAL MEDICAL EMERGENCY ADVISORY**\n\n"
    "The symptoms you described may represent a serious, life-threatening medical emergency. "
    "**DO NOT wait for an online response or attempt self-treatment.**\n\n"
    "**Immediate Actions:**\n"
    "• **United States & Canada:** Call **911** immediately.\n"
    "• **United Kingdom:** Call **999**.\n"
    "• **European Union:** Call **112**.\n"
    "• **India:** Call **112** or **108** for ambulance.\n"
    "• **Suicide & Crisis Lifeline (US/Canada):** Call or text **988**.\n\n"
    "If you or the person experiencing these symptoms are able, go to the nearest hospital Emergency Room immediately."
)

class EmergencyDetector:
    def __init__(self):
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in EMERGENCY_PATTERNS]

    def check(self, text: str) -> tuple[bool, str | None]:
        if not text:
            return False, None
        text_lower = text.lower().strip()

        # Check if this is an academic, informational, or preventive inquiry rather than an active medical crisis
        is_informational = any(
            text_lower.startswith(p) for p in [
                "what is", "what are", "what causes", "how to prevent", "how does", "why do",
                "why does", "can you explain", "tell me about", "difference between", "define"
            ]
        ) or any(
            kw in text_lower for kw in [
                "risk factors", "how to prevent", "causes of", "difference between",
                "statistics", "awareness", "prevention of"
            ]
        )

        # Do not alarm on purely theoretical questions (e.g. "What are heart attack risk factors in adults?")
        # unless active acute personal distress markers or self-harm are stated
        if is_informational and not any(w in text_lower for w in ["suicid", "kill myself", "want to die", "cannot breathe at all", "lips are turning blue"]):
            if not any(w in text_lower for w in ["i have", "my ", "i am experiencing", "i feel", "right now", "hurting"]):
                return False, None

        for pattern in self.compiled_patterns:
            if pattern.search(text_lower):
                return True, EMERGENCY_RESPONSE_MESSAGE
        return False, None
