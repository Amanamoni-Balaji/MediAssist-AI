from typing import Optional

class NLPService:
    """
    Backwards-compatible NLPService wrapper delegating to ChatbotService.
    Preserves all existing signatures and interfaces.
    """
    _instance = None

    def __init__(self):
        from chatbot.service import ChatbotService
        self.chatbot_service = ChatbotService.get_instance()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def ensure_knowledge_indexed(self):
        self.chatbot_service.rag_engine.ensure_indexed()

    def process_message(self, user_text: str, conversation_context: Optional[dict] = None, conversation_id: Optional[str] = None) -> dict:
        cid = conversation_id
        if not cid and conversation_context and "conversation_id" in conversation_context:
            cid = conversation_context["conversation_id"]

        return self.chatbot_service.process_user_message(user_text, conversation_id=cid)
