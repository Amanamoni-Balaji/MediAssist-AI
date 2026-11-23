from typing import Dict, Any, Optional
from semantic_search.searcher import HybridSemanticSearcher
from safety_engine.emergency import EmergencyDetector
from conversation_context.context_manager import ContextManager, ConversationContext
from .response_formatter import ResponseFormatter

class RAGEngine:
    _instance = None

    def __init__(self):
        self.searcher = HybridSemanticSearcher()
        self.emergency_detector = EmergencyDetector()
        self.formatter = ResponseFormatter()
        self._is_indexed = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def ensure_indexed(self):
        """Loads all records from MedicalKnowledge model into the hybrid searcher."""
        if not self._is_indexed:
            try:
                from medical_knowledge.models import MedicalKnowledge
                records = list(MedicalKnowledge.objects.all().values(
                    'id', 'topic', 'slug', 'category', 'description',
                    'symptoms', 'causes', 'prevention', 'when_to_seek_care',
                    'references', 'keywords'
                ))
                if records:
                    self.searcher.index_knowledge_base(records)
                    self._is_indexed = True
            except Exception as e:
                print(f"Warning in RAGEngine indexing: {e}")

    def query(self, raw_query: str, conversation_id: Optional[str] = None, entities: Optional[dict] = None, intent: Optional[str] = None) -> dict:
        """
        Executes complete RAG pipeline:
        1. Emergency Safety Check
        2. Everyday Conversational Filter
        3. Contextual Pronoun & Elliptical Query Resolution
        4. Hybrid Semantic Retrieval (Dense + Sparse + Entity Alignment)
        5. Tailored Clinical Response Synthesis
        6. Context State Update
        """
        cleaned_query = (raw_query or "").strip()
        if not cleaned_query:
            return {
                "response": "Please enter a health inquiry or medical question.",
                "intent": "unknown_query",
                "confidence": 0.0,
                "matched_topic": None,
                "is_emergency": False,
                "suggested_questions": ["What causes headaches?", "How to improve sleep?"]
            }

        # Step 1: Emergency Triage Check
        is_emergency, emergency_msg = self.emergency_detector.check(cleaned_query)
        if is_emergency:
            return {
                "response": emergency_msg,
                "intent": "emergency_symptoms",
                "confidence": 1.0,
                "matched_topic": "Emergency Advisory",
                "is_emergency": True,
                "suggested_questions": [
                    "What are stroke warning signs?",
                    "How to recognize a heart attack?",
                    "Emergency helpline numbers"
                ]
            }

        # Step 2: Casual Conversation Dispatcher (No Disclaimers)
        casual_intents = ["greeting", "general_conversation", "chatbot_identity", "gratitude", "farewell"]
        if intent in casual_intents:
            resp_text, suggestions = self.formatter.format_casual_chat(intent, cleaned_query)
            return {
                "response": resp_text,
                "intent": intent,
                "confidence": 0.95,
                "matched_topic": None,
                "is_emergency": False,
                "suggested_questions": suggestions
            }

        # Step 3: Conversation Context & Pronoun Resolution
        context = ContextManager.get_or_create(conversation_id) if conversation_id else None
        augmented_query, is_followup, context_meta = ContextManager.resolve_followup_query(cleaned_query, context)

        # Step 4: Ensure Knowledge Base is Indexed
        self.ensure_indexed()

        # Step 5: Hybrid Semantic Retrieval
        search_results = self.searcher.search(augmented_query, entities=entities, top_k=2)
        top_match = search_results[0] if search_results else None
        matched_record = top_match["record"] if top_match else None
        match_score = top_match["score"] if top_match else 0.0
        matched_topic = matched_record.get("topic") if matched_record else None

        # Step 6: Tailored Response Synthesis
        # A. Contextual Medication / Prevention Follow-up
        if is_followup and context_meta.get("followup_type") == "medication" and matched_record:
            resp_text, suggestions = self.formatter.format_medication_response(
                topic=context_meta.get("topic", matched_topic),
                record=matched_record,
                context_meta=context_meta
            )
        # B. Contextual Focal Hyperhidrosis Follow-up (e.g. hands and feet)
        elif matched_topic and "hyperhidrosis" in matched_topic.lower() and (context and context.focal_body_parts):
            resp_text, suggestions = self.formatter.format_hyperhidrosis_focal(
                record=matched_record,
                body_parts=context.focal_body_parts
            )
        # C. Direct Hyperhidrosis Query mentioning hands/feet
        elif matched_topic and "hyperhidrosis" in matched_topic.lower() and any(bp in cleaned_query.lower() for bp in ["hands", "feet", "palms", "underarms"]):
            found_bps = [bp for bp in ["hands", "feet", "palms", "underarms"] if bp in cleaned_query.lower()]
            resp_text, suggestions = self.formatter.format_hyperhidrosis_focal(
                record=matched_record,
                body_parts=found_bps
            )
        # D. Standard Knowledge Match (Threshold >= 0.10 or semantic entity match)
        elif matched_record and (match_score >= 0.10 or is_followup or (entities and (entities.get("conditions") or entities.get("symptoms")))):
            resp_text, suggestions = self.formatter.format_clinical_knowledge(
                record=matched_record,
                query_intent=intent or "medical_information",
                user_query=cleaned_query
            )
        # E. Intelligent Symptom Summary if user listed multiple symptoms
        elif entities and entities.get("symptoms"):
            symptoms_list = ", ".join(entities["symptoms"])
            resp_text = (
                f"### 🩺 Symptom Information Summary\n\n"
                f"You mentioned experiencing: **{symptoms_list}**.\n\n"
                f"**Clinical Context:**\n"
                f"Symptoms like {symptoms_list} can be caused by viral infections, benign temporary fatigue, or underlying muscular or metabolic factors. "
                f"Because symptoms frequently overlap between conditions, a clinical examination by a physician is necessary for accurate diagnosis.\n\n"
                f"**Supportive Measures:**\n"
                f"• Hydrate regularly with water or clear electrolyte fluids.\n"
                f"• Rest adequately and monitor symptom duration.\n"
                f"• Avoid strenuous physical strain while feeling weak.\n\n"
                f"**When to See a Doctor:** Seek professional evaluation if symptoms persist beyond 48–72 hours or rapidly worsen."
            )
            from safety_engine.disclaimers import get_disclaimer
            resp_text += get_disclaimer("symptom_inquiry")
            suggestions = [
                "What are symptoms of dehydration?",
                "What causes persistent fatigue?",
                "When to see a doctor for fever?"
            ]
        # F. Intelligent Scope Guidance (Never generic robotic fallback)
        else:
            resp_text = (
                f"### 💡 Healthcare Information Guidance\n\n"
                f"I understand your question regarding **'{cleaned_query}'**.\n\n"
                f"As an AI healthcare assistant, I can provide reliable educational insights across major healthcare domains:\n"
                f"• **Dermatology & Skin:** Excessive sweating (hyperhidrosis), acne, eczema, psoriasis, hair fall, rashes.\n"
                f"• **General Symptoms:** Fever, headaches, coughs, body pain, stomach burning, fatigue, dizziness.\n"
                f"• **Cardiovascular & Respiratory:** High/low blood pressure, cholesterol, asthma, bronchitis.\n"
                f"• **Metabolic & Endocrine:** Diabetes, thyroid health, PCOS, weight management.\n"
                f"• **Nutrition & Lifestyle:** Hemoglobin support, protein intake, hydration, sleep hygiene.\n\n"
                f"Could you share a bit more detail about your symptoms or the specific health topic you are curious about?"
            )
            from safety_engine.disclaimers import get_disclaimer
            resp_text += get_disclaimer("medical_information")
            suggestions = [
                "Why do my hands and feet sweat so much?",
                "What causes insomnia and poor sleep?",
                "What foods increase hemoglobin?",
                "How to maintain a healthy blood pressure?"
            ]

        # Step 7: Update Conversation Context
        if context:
            context.update_with_turn(
                user_text=cleaned_query,
                bot_response=resp_text,
                topic=matched_topic if match_score >= 0.10 else None,
                category=matched_record.get("category") if matched_record else None,
                entities=entities
            )

        return {
            "response": resp_text,
            "intent": intent or ("follow_up_question" if is_followup else "medical_information"),
            "confidence": round(match_score, 4),
            "matched_topic": matched_topic if match_score >= 0.10 else None,
            "is_emergency": False,
            "is_followup": is_followup,
            "suggested_questions": suggestions,
            "dense_score": top_match["dense_score"] if top_match else 0.0,
            "lexical_score": top_match["lexical_score"] if top_match else 0.0
        }
