STANDARD_DISCLAIMER = (
    "\n\n*Medical Disclaimer: This response is for educational and informational purposes only. "
    "It is not an individualized clinical diagnosis, medical prescription, or replacement for professional healthcare consultation. "
    "Always consult a qualified physician or healthcare provider for personal health concerns or persistent symptoms.*"
)

MEDICATION_DISCLAIMER = (
    "\n\n*Medication Safety Advisory: The treatments mentioned above represent general educational categories, not an individualized prescription or dosage recommendation. "
    "Different medications have interactions, side effects, and contraindications. Always consult a licensed doctor or pharmacist before starting, changing, or discontinuing any medication.*"
)

def get_disclaimer(intent: str, contains_medication: bool = False) -> str:
    """Returns the appropriate clinical disclaimer based on conversation type."""
    # Never attach disclaimers to everyday social conversations, greetings, or identity questions
    if intent in ["greeting", "general_conversation", "farewell", "gratitude", "chatbot_identity"]:
        return ""
    if contains_medication:
        return MEDICATION_DISCLAIMER
    return STANDARD_DISCLAIMER

