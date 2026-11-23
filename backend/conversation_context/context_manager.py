import re
from typing import Dict, Any, Optional

class ConversationContext:
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.active_topic: Optional[str] = None
        self.active_category: Optional[str] = None
        self.focal_symptoms: list[str] = []
        self.focal_body_parts: list[str] = []
        self.turns: list[dict] = []

    def update_with_turn(self, user_text: str, bot_response: str, topic: Optional[str] = None, category: Optional[str] = None, entities: Optional[dict] = None):
        if topic:
            self.active_topic = topic
        if category:
            self.active_category = category
        if entities:
            for s in entities.get("symptoms", []):
                if s not in self.focal_symptoms:
                    self.focal_symptoms.append(s)
            for bp in entities.get("body_parts", []):
                if bp not in self.focal_body_parts:
                    self.focal_body_parts.append(bp)

        self.turns.append({
            "user": user_text,
            "assistant": bot_response,
            "topic": self.active_topic
        })
        # Keep last 10 turns
        if len(self.turns) > 10:
            self.turns = self.turns[-10:]

    def to_dict(self) -> dict:
        return {
            "conversation_id": self.conversation_id,
            "active_topic": self.active_topic,
            "active_category": self.active_category,
            "focal_symptoms": self.focal_symptoms,
            "focal_body_parts": self.focal_body_parts,
            "turn_count": len(self.turns)
        }


class ContextManager:
    """
    Manages in-memory and database session context across turns.
    Resolves anaphoric pronouns, elliptical questions, and follow-up references.
    """
    _sessions: Dict[str, ConversationContext] = {}

    @classmethod
    def get_or_create(cls, conversation_id: str) -> ConversationContext:
        if conversation_id not in cls._sessions:
            cls._sessions[conversation_id] = ConversationContext(conversation_id)
        return cls._sessions[conversation_id]

    @classmethod
    def resolve_followup_query(cls, raw_query: str, context: Optional[ConversationContext]) -> tuple[str, bool, dict]:
        """
        Inspects query for pronouns ('it', 'this', 'that', 'these') or elliptical phrasing
        ('What can I take?', 'Give medicines to prevent', 'How can I control it?', 'What causes this?').
        Returns (augmented_query, is_followup, context_meta).
        """
        if not context or not context.active_topic:
            return raw_query, False, {}

        q_clean = raw_query.strip()
        q_lower = q_clean.lower()
        topic = context.active_topic

        # Detect body parts specified in the follow-up (e.g. "It happens mostly on my hands and feet")
        body_parts_found = []
        for bp in ["hands", "feet", "palms", "soles", "underarms", "armpits", "face", "chest", "stomach", "legs", "back", "joints", "skin"]:
            if re.search(r'\b' + re.escape(bp) + r'\b', q_lower):
                body_parts_found.append(bp)
                if bp not in context.focal_body_parts:
                    context.focal_body_parts.append(bp)

        is_followup = False
        augmented = q_clean

        # Pattern 1: Medication / Treatment inquiry without explicit topic
        # e.g., "Give medicines to prevent", "What can I take?", "What medicine should I use?", "Any medication?"
        med_match = re.search(r'\b(?:what\s+(?:can|should)\s+i\s+take|give\s+medicines?|what\s+medicines?|how\s+to\s+cure|how\s+to\s+treat|treatment\s+options?|what\s+can\s+help|any\s+tablets?|home\s+remedies?|remedy)\b', q_lower)
        if med_match:
            is_followup = True
            augmented = f"treatment medication relief options for {topic}"
            if body_parts_found:
                augmented += f" on {' and '.join(body_parts_found)}"
            return augmented, True, {"followup_type": "medication", "topic": topic}

        # Pattern 2: Management / Control inquiry
        # e.g., "How can I control it?", "How to stop it?", "How to prevent this?"
        control_match = re.search(r'\b(?:how\s+(?:can\s+i|to)\s+(?:control|stop|prevent|manage|handle|deal\s+with))\s+(?:it|this|that|these|them)?\b', q_lower)
        if control_match:
            is_followup = True
            augmented = f"how to manage control and prevent {topic}"
            if body_parts_found or context.focal_body_parts:
                bps = body_parts_found or context.focal_body_parts
                augmented += f" on {' and '.join(bps)}"
            return augmented, True, {"followup_type": "control", "topic": topic}

        # Pattern 3: Causes inquiry with pronoun
        # e.g., "What causes this?", "Why does it happen?", "What triggers that?"
        cause_match = re.search(r'\b(?:what\s+causes?|why\s+does\s+it\s+happen|what\s+triggers?)\s+(?:this|it|that)?\b', q_lower)
        if cause_match:
            is_followup = True
            augmented = f"causes and triggers of {topic}"
            return augmented, True, {"followup_type": "causes", "topic": topic}

        # Pattern 4: Symptom clarification / location specification
        # e.g., "It happens mostly on my hands and feet", "It is on my stomach"
        location_spec_match = re.search(r'\b(?:it\s+(?:happens|is|occurs|starts)\s+(?:mostly\s+)?(?:on|in|at)\s+my|on\s+my|in\s+my)\s+([a-zA-Z\s]+)\b', q_lower)
        if location_spec_match and body_parts_found:
            is_followup = True
            augmented = f"{topic} affecting {' and '.join(body_parts_found)}"
            return augmented, True, {"followup_type": "location_specification", "topic": topic, "body_parts": body_parts_found}

        # Pattern 5: General pronoun substitution
        pronoun_patterns = [
            (r'\b(?:its|it\'s)\s+symptoms\b', f"symptoms of {topic}"),
            (r'\bmore\s+about\s+(?:it|this|that)\b', f"more information on {topic}"),
            (r'\bexplain\s+(?:it|this|that)\s+in\s+simple\s+words\b', f"explain {topic} simply"),
            (r'\bwhen\s+to\s+see\s+a\s+doctor\s+for\s+(?:it|this|that)\b', f"when to see doctor for {topic}")
        ]
        for pat, repl in pronoun_patterns:
            if re.search(pat, q_lower):
                is_followup = True
                augmented = re.sub(pat, repl, q_clean, flags=re.IGNORECASE)
                return augmented, True, {"followup_type": "pronoun_replacement", "topic": topic}

        # If query is very short (< 4 words) and contains pronouns "it", "this", "that"
        if len(q_clean.split()) <= 4 and any(w in q_lower.split() for w in ["it", "this", "that"]):
            is_followup = True
            augmented = f"{q_clean} {topic}"
            return augmented, True, {"followup_type": "context_expansion", "topic": topic}

        return raw_query, False, {}

