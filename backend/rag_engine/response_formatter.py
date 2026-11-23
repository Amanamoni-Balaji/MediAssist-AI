from safety_engine.disclaimers import get_disclaimer

GREETING_RESPONSES = (
    "Hello! I am **Dr. MediNLP**, your intelligent AI Medical & Healthcare Information Assistant. "
    "I can help you understand symptoms, medical conditions, sleep wellness, skin health, nutrition, and healthy living.\n\n"
    "What health or wellness question can I assist you with today?"
)

CONVERSATION_RESPONSES = (
    "I'm doing well, thank you for asking! I'm actively analyzing healthcare queries and ready to assist you. "
    "How are you feeling today, and what health topic would you like to explore?"
)

IDENTITY_RESPONSE = (
    "### 🩺 About Dr. MediNLP AI Assistant\n\n"
    "I am **Dr. MediNLP**, an intelligent healthcare information assistant developed using Natural Language Processing (NLP), Semantic Embeddings, and Machine Learning.\n\n"
    "**Core Capabilities Across Healthcare Domains:**\n"
    "• **Dermatology & Skin:** Hyperhidrosis (excessive sweating of hands/feet), acne, eczema, psoriasis, hair fall, fungal rashes.\n"
    "• **General Medicine:** Fever, cold, cough, headaches, migraines, stomach pain, dizziness, fatigue, allergies.\n"
    "• **Cardiovascular & Respiratory:** Hypertension, cholesterol, asthma, bronchitis, breathing difficulties.\n"
    "• **Endocrine & Metabolic:** Type 2 diabetes, thyroid disorders, PCOS, weight management.\n"
    "• **Mental Wellness & Sleep:** Insomnia, sleep hygiene, stress reduction, anxiety awareness.\n"
    "• **Nutrition & Lifestyle:** Hemoglobin support, iron intake, dietary protein, balanced nutrition, exercise.\n"
    "• **Medical Education:** Differences between viruses and bacteria, human body physiology, first aid.\n\n"
    "**Clinical Boundary:** I provide evidence-based educational insights and **cannot prescribe individual medications or replace a licensed medical doctor**."
)

INTERESTING_FACTS = (
    "### 💡 Fascinating Medical Fact\n\n"
    "Did you know? **Your skin is your body's largest organ**, containing approximately 2 to 4 million sweat glands! "
    "Most of these are eccrine sweat glands, with their highest density on the palms of your hands and the soles of your feet (up to 600–700 glands per square centimeter)—which is why emotional stress or hyperhidrosis often manifests first in sweaty hands and feet."
)

class ResponseFormatter:
    """
    Synthesizes tailored, modular markdown responses based on matched clinical knowledge,
    query intent, and conversational context.
    """

    @staticmethod
    def format_casual_chat(intent: str, query: str) -> tuple[str, list[str]]:
        """Handles everyday human conversations without clinical disclaimers."""
        q_lower = query.lower()
        if intent == "greeting":
            return GREETING_RESPONSES, [
                "My hands and feet sweat too much",
                "I have cold and cough",
                "I cannot sleep properly",
                "What is the difference between bacteria and viruses?"
            ]
        elif intent == "chatbot_identity":
            return IDENTITY_RESPONSE, [
                "What medical topics do you cover?",
                "How do you protect my privacy?",
                "What can I do for excessive sweating?",
                "Tips for improving sleep quality"
            ]
        elif intent == "general_conversation":
            if "interesting" in q_lower or "fact" in q_lower:
                return INTERESTING_FACTS, [
                    "How does the immune system work?",
                    "How much water should I drink daily?",
                    "What are benefits of daily walking?"
                ]
            return CONVERSATION_RESPONSES, [
                "What topics can you help me with?",
                "My hands and feet sweat a lot",
                "What foods increase hemoglobin?",
                "How to manage stress?"
            ]
        elif intent == "gratitude":
            return "You are very welcome! I'm glad I could provide helpful educational information. If you have any further health questions, feel free to ask anytime. Stay healthy and take care!", [
                "Explore symptom guide", "Read about nutrition", "Tips for healthy sleep"
            ]
        elif intent == "farewell":
            return "Take good care of yourself! Remember to stay hydrated, active, and consult a qualified healthcare provider for any persistent symptoms. Wishing you vitality and good health!", [
                "How to improve sleep?", "Tips for balanced diet"
            ]
        return "I am here and ready to help with your health questions. What would you like to know?", ["What is diabetes?", "What causes headaches?"]

    @staticmethod
    def format_medication_response(topic: str, record: dict, context_meta: dict) -> tuple[str, list[str]]:
        """Synthesizes educational medication & general treatment categories with safety warnings."""
        prevention_info = record.get("prevention", "")
        when_to_seek = record.get("when_to_seek_care", "")
        refs = record.get("references", [])

        # Check if viral condition like cold/flu
        is_viral = any(w in topic.lower() for w in ["cold", "viral", "influenza", "flu"])

        response = f"### 💊 General Management & Treatment Categories: {topic}\n\n"
        response += f"Regarding relief and management options for **{topic}**:\n\n"

        if is_viral:
            response += (
                "**⚠️ Important Clinical Rule Regarding Viral Infections:**\n"
                "• **Antibiotics DO NOT work against viral colds or viral coughs.** Antibiotics kill bacteria, not viruses. "
                "Taking antibiotics for a viral infection provides zero benefit and can cause adverse side effects and antibiotic resistance.\n\n"
            )

        response += f"**Evidence-Based Supportive Care & Treatment Categories:**\n{prevention_info}\n\n"
        response += (
            "**Safe Medication Guidance:**\n"
            "• Over-the-counter options (such as antipyretics, saline rinses, or barrier antiperspirants) should always be selected with guidance from a licensed pharmacist or doctor.\n"
            "• Individual dosages and treatment courses depend on age, weight, liver/kidney function, and concurrent medications.\n\n"
            f"**When to See a Doctor:**\n{when_to_seek}"
        )

        if refs:
            response += "\n\n**Reliable Clinical References:**\n"
            for r in refs:
                response += f"- [{r.get('source')} - {r.get('title')}]({r.get('url')})\n"

        response += get_disclaimer("treatment_information", contains_medication=True)

        suggested = [
            f"What causes {topic}?",
            f"What are common symptoms of {topic}?",
            f"When should I see a doctor for {topic}?",
            "How can lifestyle changes help?"
        ]
        return response, suggested

    @staticmethod
    def format_hyperhidrosis_focal(record: dict, body_parts: list[str]) -> tuple[str, list[str]]:
        """Specialized focal response for hyperhidrosis affecting hands, feet, or underarms."""
        bps_str = " and ".join(body_parts) if body_parts else "hands and feet"
        topic = record.get("topic", "Hyperhidrosis")
        desc = record.get("description", "")
        prevention = record.get("prevention", "")
        when_to_seek = record.get("when_to_seek_care", "")
        refs = record.get("references", [])

        response = (
            f"### 🩺 Understanding Excessive Sweating on the {bps_str.title()} (Focal Hyperhidrosis)\n\n"
            f"Excessive sweating that predominantly affects the **{bps_str}** is clinically recognized as **focal hyperhidrosis** "
            f"(specifically palmar hyperhidrosis for palms, and plantar hyperhidrosis for soles).\n\n"
            f"**Why the {bps_str.title()}?**\n"
            f"The human palms and soles contain the highest concentration of eccrine sweat glands on the entire body. "
            f"In focal hyperhidrosis, the sympathetic nervous system triggers these sweat glands to overproduce sweat even during cool conditions or when resting.\n\n"
            f"**Targeted Management for {bps_str.title()}:**\n"
            f"1. **Clinical-Strength Antiperspirants:** Aluminum chloride hexahydrate formulations (15–20%) applied to completely dry palms or soles at night before sleep.\n"
            f"2. **Iontophoresis Therapy:** A proven, drug-free medical treatment where hands or feet are placed in shallow water trays while a mild, painless electrical current temporarily blocks sweat channels.\n"
            f"3. **Footwear & Skin Care:** Moisture-wicking socks (merino wool or specialized athletic fibers), changing socks 2 times daily, and using absorbent foot powders to prevent fungal maceration.\n"
            f"4. **Prescription Options (Dermatologist):** Botulinum toxin (Botox) injections to temporarily paralyze sweat gland innervation, or oral anticholinergic medications.\n\n"
            f"**When to Consult a Physician:**\n{when_to_seek}"
        )

        if refs:
            response += "\n\n**Reliable Clinical References:**\n"
            for r in refs:
                response += f"- [{r.get('source')} - {r.get('title')}]({r.get('url')})\n"

        response += get_disclaimer("medical_information")

        suggested = [
            f"How can I control excessive sweating on my {bps_str}?",
            "What is iontophoresis and how does it work?",
            "What causes primary focal hyperhidrosis?",
            "When should I see a dermatologist for sweating?"
        ]
        return response, suggested

    @staticmethod
    def format_clinical_knowledge(record: dict, query_intent: str, user_query: str) -> tuple[str, list[str]]:
        """Standard modular clinical response synthesis with source citations."""
        topic = record.get("topic", "")
        category = record.get("category", "")
        desc = record.get("description", "")
        symptoms = record.get("symptoms", [])
        causes = record.get("causes", "")
        prevention = record.get("prevention", "")
        when_to_seek = record.get("when_to_seek_care", "")
        refs = record.get("references", [])

        symptoms_md = "\n".join([f"• {s}" for s in symptoms]) if isinstance(symptoms, list) else f"• {symptoms}"

        if query_intent == "symptom_inquiry":
            response = (
                f"### 📋 Symptoms & Characteristics of {topic}\n\n"
                f"**Clinical Category:** {category}\n\n"
                f"{desc}\n\n"
                f"**Key Clinical Symptoms to Monitor:**\n{symptoms_md}\n\n"
                f"**Underlying Causes & Triggers:**\n{causes}\n\n"
                f"**⚠️ When to Seek Medical Attention:**\n{when_to_seek}"
            )
        elif query_intent == "cause_inquiry":
            response = (
                f"### 🔍 Causes & Triggers of {topic}\n\n"
                f"**Overview:** {desc}\n\n"
                f"**Primary Causes & Contributing Factors:**\n{causes}\n\n"
                f"**Associated Symptoms:**\n{symptoms_md}\n\n"
                f"**Prevention & Risk Reduction:**\n{prevention}"
            )
        elif query_intent == "treatment_information":
            response = (
                f"### 💊 Management & Care Options for {topic}\n\n"
                f"**Clinical Overview:** {desc}\n\n"
                f"**Evidence-Based Management & Self-Care:**\n{prevention}\n\n"
                f"**⚠️ Warning Signs & Clinical Evaluation:**\n{when_to_seek}"
            )
        else:
            response = (
                f"### 🩺 Clinical Overview: {topic}\n\n"
                f"**Category:** {category}\n\n"
                f"{desc}\n\n"
                f"**Common Associated Symptoms:**\n{symptoms_md}\n\n"
                f"**Possible Causes:**\n{causes}\n\n"
                f"**General Management & Prevention:**\n{prevention}\n\n"
                f"**⚠️ When to Seek Professional Care:**\n{when_to_seek}"
            )

        if refs:
            response += "\n\n**Reliable Medical References:**\n"
            for r in refs:
                response += f"- [{r.get('source')} - {r.get('title')}]({r.get('url')})\n"

        response += get_disclaimer("medical_information")

        suggested = [
            f"What causes {topic}?",
            f"How to control or manage {topic}?",
            f"What are the warning signs of {topic}?",
            "When should I consult a doctor?"
        ]
        return response, suggested

