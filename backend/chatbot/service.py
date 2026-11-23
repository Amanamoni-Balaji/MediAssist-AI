from typing import Optional
from nlp_engine.preprocessor import TextPreprocessor
from nlp_engine.intent_classifier import IntentClassifier
from nlp_engine.entity_extractor import MedicalEntityExtractor
from rag_engine.engine import RAGEngine

class ChatbotService:
    """
    Central AI Healthcare Chatbot Coordinator.
    Coordinates Preprocessing, Intent Classification, Entity Extraction,
    and Retrieval-Augmented Generation (RAG).
    """
    _instance = None

    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = MedicalEntityExtractor()
        self.rag_engine = RAGEngine.get_instance()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def process_user_message(self, user_text: str, conversation_id: Optional[str] = None) -> dict:
        """
        Processes a user message end-to-end:
        1. Clean and normalize input
        2. Classify intent
        3. Extract medical entities
        4. Execute RAG query with conversational context
        """
        raw_text = (user_text or "").strip()
        if not raw_text:
            return {
                "response": "Please enter a health inquiry or medical question.",
                "intent": "unknown_query",
                "confidence": 0.0,
                "entities": {},
                "is_emergency": False,
                "matched_topic": None,
                "suggested_questions": ["What is hyperhidrosis?", "What causes headaches?"]
            }

        # Step 1: Preprocessing & Entity Extraction
        entities = self.entity_extractor.extract(raw_text)

        # Step 2: Intent Classification
        predicted_intent, confidence, prob_dict = self.intent_classifier.predict(raw_text)

        # Step 3: RAG Engine with Context Resolution
        rag_result = self.rag_engine.query(
            raw_query=raw_text,
            conversation_id=conversation_id,
            entities=entities,
            intent=predicted_intent
        )

        return {
            "response": rag_result["response"],
            "intent": rag_result.get("intent", predicted_intent),
            "confidence": rag_result.get("confidence", confidence),
            "entities": entities,
            "is_emergency": rag_result.get("is_emergency", False),
            "matched_topic": rag_result.get("matched_topic"),
            "suggested_questions": rag_result.get("suggested_questions", []),
            "probabilities": prob_dict,
            "is_followup": rag_result.get("is_followup", False)
        }

