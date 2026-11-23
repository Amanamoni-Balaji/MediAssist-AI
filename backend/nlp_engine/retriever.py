import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessor import TextPreprocessor

STANDARD_DISCLAIMER = (
    "\n\n*Medical Disclaimer: This response is for educational and informational purposes only. "
    "It is not a clinical diagnosis, medical prescription, or replacement for professional healthcare consultation. "
    "Always consult a qualified physician or healthcare provider for personal health concerns or persistent symptoms.*"
)

# Friendly conversational responses
GREETING_RESPONSES = (
    "Hello! I am **Dr. MediNLP**, your AI Medical & Healthcare Information Assistant. "
    "I'm here to provide evidence-based educational insights regarding common medical conditions, symptoms, sleep wellness, nutrition, and healthy living.\n\n"
    "How can I help you today?"
)

GENERAL_CONVERSATION_RESPONSES = [
    (
        "I'm doing well, thank you for asking! I'm actively running, analyzing healthcare data, and ready to assist you. "
        "How are you feeling today, and what health topic would you like to explore?"
    ),
    (
        "I'm ready and glad to chat! As an AI healthcare assistant, I'm here to answer questions about symptoms, healthy habits, sleep, nutrition, and human biology. "
        "What's on your mind today?"
    )
]

IDENTITY_RESPONSE = (
    "### 🩺 About Dr. MediNLP AI Assistant\n\n"
    "I am **Dr. MediNLP**, an intelligent healthcare information assistant developed using Natural Language Processing (NLP) and Machine Learning.\n\n"
    "**What I Can Do:**\n"
    "• **Symptom Awareness:** Explain what common symptoms mean (headaches, fever, cough, stomach pain, fatigue).\n"
    "• **Condition Guides:** Provide verified educational overviews of conditions like diabetes, hypertension, asthma, anemia, thyroid disorders, and digestive health.\n"
    "• **Sleep & Mental Wellness:** Offer evidence-based sleep hygiene tips and stress management techniques.\n"
    "• **Nutrition & Lifestyle:** Detail balanced diets, protein intake, hemoglobin support, hydration, and exercise.\n"
    "• **Health Education:** Explain how human body systems work and clarify differences between viruses and bacteria.\n\n"
    "**Important Boundary:** I am an educational resource, **not a licensed doctor**. I cannot provide personal clinical diagnoses or prescribe medications."
)

FAREWELL_RESPONSES = (
    "Take good care of yourself! Remember to stay hydrated, get restful sleep, and consult a qualified physician if you experience persistent or concerning symptoms. Wishing you vitality and good health!"
)

GRATITUDE_RESPONSES = (
    "You are very welcome! I'm glad I could provide helpful educational information. If you ever have more health questions or need clarification, feel free to ask anytime. Stay healthy and take care!"
)

INTERESTING_FACTS = (
    "### 💡 Fascinating Human Body Fact\n\n"
    "Did you know? **Your heart beats approximately 100,000 times every single day**, pumping about 2,000 gallons (7,570 liters) of blood through 60,000 miles of blood vessels! "
    "Also, your gut microbiome houses trillions of microbes that produce neurotransmitters like serotonin, meaning gut health directly influences mood and sleep."
)


class KnowledgeRetriever:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        self.corpus_docs = []
        self.knowledge_records = []
        self.tfidf_matrix = None

    def index_knowledge(self, records: list):
        """Indexes a list of MedicalKnowledge model instances or dicts."""
        self.knowledge_records = records
        self.corpus_docs = []

        for rec in records:
            # Combine topic, keywords, symptoms, description, causes, prevention into a rich corpus string
            symptoms_str = " ".join(rec.get('symptoms', [])) if isinstance(rec.get('symptoms'), list) else str(rec.get('symptoms', ''))
            full_text = f"{rec.get('topic', '')} {rec.get('keywords', '')} {symptoms_str} {rec.get('description', '')} {rec.get('causes', '')} {rec.get('prevention', '')}"
            processed = self.preprocessor.preprocess(full_text)
            self.corpus_docs.append(processed)

        if self.corpus_docs:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus_docs)

    def retrieve_best_match(self, query: str, top_k: int = 1) -> list[tuple[dict, float]]:
        """Computes cosine similarity between query and knowledge corpus."""
        if not self.corpus_docs or self.tfidf_matrix is None:
            return []

        processed_query = self.preprocessor.preprocess(query)
        if not processed_query:
            return []

        query_vec = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        ranked_indices = similarities.argsort()[::-1][:top_k]
        results = []
        for idx in ranked_indices:
            score = float(similarities[idx])
            results.append((self.knowledge_records[idx], round(score, 4)))

        return results

    # ==========================================
    # SPECIALIZED CLINICAL INTENT HANDLERS
    # ==========================================

    def _handle_sleep_inquiry(self, query: str) -> tuple[str, list[str]]:
        """Intelligent response for sleep difficulties, insomnia, and poor sleep."""
        response = (
            "### 🌙 Understanding Sleep Difficulties & Insomnia\n\n"
            "I'm sorry to hear that you are having trouble sleeping. Restorative sleep is fundamental for brain function, immune strength, and cellular recovery.\n\n"
            "**Common Everyday Causes of Sleeplessness:**\n"
            "• **Evening Screen Exposure:** Blue light emitted by phones, tablets, and monitors suppresses melatonin, your body's natural sleep-inducing hormone.\n"
            "• **Caffeine & Stimulants:** Consuming coffee, tea, pre-workout, or energy drinks within 6 hours of bedtime.\n"
            "• **Stress & Racing Thoughts:** Mental anxiety elevates cortisol and keeps your nervous system in an alert state.\n"
            "• **Irregular Sleep Schedule:** Sleeping and waking at varying times disrupts your circadian rhythm.\n"
            "• **Environment:** A room that is too warm, noisy, or bright prevents deep restorative sleep stages.\n\n"
            "**Evidence-Based Sleep Hygiene Steps:**\n"
            "1. **Fixed Sleep-Wake Routine:** Go to bed and wake up at the exact same time every day, even on weekends.\n"
            "2. **The 20-Minute Rule:** If you are unable to fall asleep after 20 minutes in bed, get up and sit in dim lighting with a book or calm activity until sleepy. Don't lie in bed tossing and turning.\n"
            "3. **Cool, Dark Sanctuary:** Keep your bedroom cool (around 18–20°C / 65–68°F) and completely dark.\n"
            "4. **Wind-Down Buffer:** Dedicate 30–60 minutes before bed to no screens, gentle stretching, or warm herbal tea (like chamomile).\n"
            "5. **Morning Sunlight:** Get 15–30 minutes of natural sunlight soon after waking up to set your circadian clock.\n\n"
            "**Clarifying Questions:**\n"
            "*How long have you been experiencing difficulty sleeping? Did it start recently due to a specific stressor, or has it been ongoing for weeks?*\n\n"
            "**⚠️ When to Consult a Doctor:** If sleeplessness persists for more than 3 to 4 weeks, causes daytime drowsiness, or is accompanied by loud snoring or gasping, consult a physician or sleep specialist."
        )
        response += STANDARD_DISCLAIMER
        suggested = [
            "What is good sleep hygiene?",
            "How does caffeine affect sleep?",
            "Can stress cause physical fatigue?",
            "When should I see a doctor for insomnia?"
        ]
        return response, suggested

    def _handle_stomach_pain_inquiry(self, query: str) -> tuple[str, list[str]]:
        """Intelligent response for stomach pain, abdominal discomfort, and gastritis."""
        response = (
            "### 🩺 Understanding Stomach & Abdominal Pain\n\n"
            "I understand that experiencing stomach discomfort is distressing. Abdominal pain can range from mild, transient digestive upsets to conditions needing medical review.\n\n"
            "**Helpful Questions to Understand the Discomfort:**\n"
            "• **Location:** Is the discomfort in your upper stomach (epigastric), lower abdomen, left side, right side, or generalized across the whole belly?\n"
            "• **Quality of Pain:** Does it feel like a sharp ache, dull cramp, gas bloating, or a burning sensation?\n"
            "• **Timing:** Did the pain start shortly after eating certain spicy, fatty, or acidic foods, or on an empty stomach?\n"
            "• **Accompanying Signs:** Are you noticing nausea, vomiting, fever, acid reflux, diarrhea, or constipation?\n\n"
            "**Common Non-Emergency Causes:**\n"
            "• Trapped intestinal gas or indigestion (dyspepsia)\n"
            "• Mild gastritis or acid reflux (GERD)\n"
            "• Food intolerance or mild gastroenteritis\n"
            "• Abdominal muscle strain or stress-related gut tension\n\n"
            "**Safe Self-Care Measures:**\n"
            "• Sip water or clear electrolyte fluids slowly to maintain hydration.\n"
            "• Eat light, bland foods (like bananas, rice, applesauce, or crackers) and avoid heavy, greasy meals.\n"
            "• Avoid lying completely flat immediately after eating.\n"
            "• **Caution:** Avoid taking NSAID pain relievers (like ibuprofen or aspirin) on an upset stomach, as they can irritate the stomach lining.\n\n"
            "**🚨 Warning Red Flags (Seek Immediate Medical Care):**\n"
            "Go to an emergency facility if your stomach pain is sudden and severe, radiates to your back or shoulder, or is accompanied by high fever, persistent vomiting, blood in vomit, or dark tarry stools."
        )
        response += STANDARD_DISCLAIMER
        suggested = [
            "What foods soothe an upset stomach?",
            "What causes acid reflux and heartburn?",
            "What are red-flag symptoms for stomach pain?",
            "How to prevent indigestion naturally?"
        ]
        return response, suggested

    def _handle_hemoglobin_inquiry(self, query: str) -> tuple[str, list[str]]:
        """Intelligent response for hemoglobin, iron, and anemia awareness."""
        response = (
            "### 🩸 How to Support Healthy Hemoglobin Levels\n\n"
            "**What is Hemoglobin?**\n"
            "Hemoglobin is an iron-rich protein in your red blood cells responsible for carrying oxygen from your lungs to tissues and organs throughout your entire body. "
            "When hemoglobin or iron stores are low, tissues receive less oxygen, leading to fatigue, pale skin, cold hands, and shortness of breath.\n\n"
            "**Evidence-Based Nutritional Strategies:**\n\n"
            "**1. Incorporate Iron-Rich Foods:**\n"
            "• **Heme Iron (Higher absorption rate):** Lean poultry, fish, eggs, and lean meats.\n"
            "• **Non-Heme Iron (Plant-based):** Spinach, kale, lentils, chickpeas, black beans, pumpkin seeds, tofu, and fortified cereals.\n\n"
            "**2. Pair Iron with Vitamin C (Crucial!):**\n"
            "• Vitamin C significantly boosts non-heme plant iron absorption. Squeeze lemon on salads, or pair lentils with bell peppers, tomatoes, broccoli, or oranges.\n\n"
            "**3. Don't Overlook Folate (B9) and Vitamin B12:**\n"
            "• Red blood cell maturation requires folate (found in leafy greens, avocados, beans) and Vitamin B12 (found in eggs, dairy, or fortified nutritional yeast).\n\n"
            "**4. Avoid Iron Blockers Around Meals:**\n"
            "• Tannins in **black tea and coffee**, as well as high-dose calcium supplements, inhibit iron absorption. Wait at least 1 to 2 hours after meals before having coffee or tea.\n\n"
            "**⚠️ Recommended Next Step:** Before taking high-dose iron supplements, have your physician order a **Complete Blood Count (CBC) and Serum Ferritin test**. "
            "Supplementing without a confirmed deficiency can lead to iron overload, so medical guidance is recommended."
        )
        response += STANDARD_DISCLAIMER
        suggested = [
            "What are common symptoms of anemia?",
            "What are good plant-based sources of iron?",
            "What causes low hemoglobin in adults?",
            "How does Vitamin C help iron absorption?"
        ]
        return response, suggested

    def _handle_virus_vs_bacteria(self, query: str) -> tuple[str, list[str]]:
        """Intelligent comparative response on viruses versus bacteria."""
        response = (
            "### 🔬 Difference Between Viruses and Bacteria\n\n"
            "While both viruses and bacteria are microscopic pathogens that can cause infections, they are biologically completely different entities:\n\n"
            "| Feature | Bacteria | Viruses |\n"
            "| :--- | :--- | :--- |\n"
            "| **Nature** | Single-celled **living organisms** with their own cellular machinery. | Non-living genetic material (DNA or RNA) enclosed in a protein coat. |\n"
            "| **Reproduction** | Can survive and reproduce independently through fission on surfaces or in bodies. | Cannot replicate on their own; must invade living host cells to multiply. |\n"
            "| **Size** | Microscopic (~1,000 nanometers) — much larger than viruses. | Extremely tiny (20 to 400 nanometers) — 10 to 100 times smaller than bacteria. |\n"
            "| **Treatment** | Treated with **Antibiotics** (which kill or stop bacterial growth). | **Antibiotics DO NOT work.** Managed with rest, fluids, antivirals, and vaccines. |\n"
            "| **Beneficial Forms** | Most bacteria are harmless or beneficial (e.g. gut flora, cheese production). | Most recognized viruses cause disease in their specific host. |\n"
            "| **Examples** | Strep throat, urinary tract infections (UTI), bacterial pneumonia, salmonella. | Common cold, influenza (flu), COVID-19, chickenpox, measles. |\n\n"
            "**Critical Medical Fact:** Taking antibiotics for viral infections like the common cold or flu **does not work** and contributes to dangerous global antibiotic resistance."
        )
        response += STANDARD_DISCLAIMER
        suggested = [
            "Why do antibiotics not work on colds?",
            "How does the immune system fight viruses?",
            "What is the difference between cold and flu?",
            "How do vaccines protect against infections?"
        ]
        return response, suggested

    def _handle_simplification(self, previous_topic: str | None, previous_text: str | None) -> tuple[str, list[str]]:
        """Simplifies the medical explanation into plain English and intuitive analogies."""
        topic_clean = (previous_topic or "").lower()

        if "hypertension" in topic_clean or "blood pressure" in topic_clean:
            analogy = (
                "### 💡 High Blood Pressure in Super Simple Words\n\n"
                "Think of your blood vessels like garden water hoses, and your heart as the water pump.\n\n"
                "• When you turn on the faucet, water flows smoothly through the hose.\n"
                "• But if someone pinches the hose, or if the water pressure is turned up way too high all the time, the walls of the hose stretch and strain.\n"
                "• Over years, that constant high pressure can wear out the pump (your heart) and damage the delicate hoses (vessels in your brain and kidneys).\n\n"
                "**What keeps the pressure normal?** Eating less salt, walking regularly, managing stress, and drinking plenty of water!"
            )
        elif "diabetes" in topic_clean:
            analogy = (
                "### 💡 Diabetes in Super Simple Words\n\n"
                "Think of your body's cells as little houses that need energy (glucose) to survive, and insulin as the key that unlocks the door.\n\n"
                "• In a healthy body, you eat food, your body makes insulin (keys), the door unlocks, and sugar goes inside the cells to give you energy.\n"
                "• In **Type 2 Diabetes**, the locks on the doors get rusty (this is called *insulin resistance*). Even though you have keys, the doors don't open easily.\n"
                "• Because sugar can't get into the houses, it piles up in the streets (your bloodstream).\n\n"
                "**What helps fix the locks?** Regular physical movement (which naturally unlocks the doors without keys!), eating high-fiber foods, and maintaining a healthy weight."
            )
        elif "asthma" in topic_clean:
            analogy = (
                "### 💡 Asthma in Super Simple Words\n\n"
                "Imagine your airways (the breathing tubes in your lungs) are like wide drinking straws.\n\n"
                "• When asthma flares up, the inside of the straw swells up, makes sticky mucus, and the muscles around the outside squeeze tight.\n"
                "• Trying to breathe feels like breathing through a very thin coffee stirrer.\n\n"
                "**What helps?** Avoiding triggers like dust, cold air, or smoke, and using doctor-prescribed inhalers that relax the squeezed muscles and open the straw right back up."
            )
        elif "sleep" in topic_clean or "insomnia" in topic_clean:
            analogy = (
                "### 💡 Sleep Difficulties in Simple Words\n\n"
                "Think of your brain like a smartphone with 50 apps open in the background.\n\n"
                "• If you keep running heavy apps (bright phone screens, caffeine, stressful thoughts) right up until bedtime, the battery stays hot and the processor won't shut down.\n"
                "• To sleep, your brain needs a **cool-down routine**: dim lights 30 minutes before bed, put the phone in another room, and keep the bedroom cool.\n"
                "• If you're tossing and turning for more than 20 minutes, get out of bed and read under a soft lamp until you feel drowsy!"
            )
        else:
            analogy = (
                "### 💡 Let's Break It Down Simply\n\n"
                "I'm happy to simplify! Medical terms can often sound overly complex, but health principles are straightforward:\n\n"
                "• **Your Body as an Engine:** It requires clean fuel (balanced nutrition and water), daily movement (exercise to circulate blood), and regular downtime (7–9 hours of sleep to repair tissues).\n"
                "• **Symptoms as Dashboard Warning Lights:** Symptoms like headache, fever, or pain are simply your body's check-engine lights telling you to rest, hydrate, or seek medical advice if they persist.\n\n"
                "What specific topic or concept would you like me to explain with a simple everyday analogy?"
            )

        analogy += STANDARD_DISCLAIMER
        suggested = [
            "What is diabetes?",
            "What causes hypertension?",
            "Tips to improve sleep naturally",
            "How does exercise benefit the heart?"
        ]
        return analogy, suggested

    # ==========================================
    # MAIN RESPONSE FORMATTER
    # ==========================================

    def format_educational_response(
        self,
        intent: str,
        query: str,
        entities: dict,
        matched_record: dict | None,
        similarity_score: float,
        conversation_context: dict | None = None
    ) -> tuple[str, list[str]]:
        """
        Generates structured, professional markdown response based on intent and matched knowledge.
        Returns (response_text, suggested_followup_questions).
        """
        query_lower = (query or "").lower()

        # 1. Specialized Intent Dispatchers
        if intent == "greeting":
            return GREETING_RESPONSES, [
                "I didn't get sleep last night",
                "What is hypertension?",
                "What is the difference between virus and bacteria?",
                "How to increase hemoglobin?"
            ]

        if intent == "general_conversation":
            if "interesting" in query_lower or "fact" in query_lower:
                return INTERESTING_FACTS, [
                    "How does the immune system work?",
                    "How much water should I drink daily?",
                    "What are benefits of daily walking?"
                ]
            import random
            resp = random.choice(GENERAL_CONVERSATION_RESPONSES)
            return resp, [
                "What topics can you help me with?",
                "How to improve sleep quality?",
                "What foods boost hemoglobin?"
            ]

        if intent == "chatbot_identity":
            return IDENTITY_RESPONSE, [
                "What topics do you cover?",
                "What is a balanced diet?",
                "How do you protect patient privacy?",
                "What are symptoms of migraine?"
            ]

        if intent == "farewell":
            return FAREWELL_RESPONSES, ["How to improve sleep?", "Tips for balanced diet"]

        if intent == "gratitude":
            return GRATITUDE_RESPONSES, ["Explore symptom guide", "Read about nutrition", "How to manage stress?"]

        if intent == "clarification_simplification":
            prev_topic = conversation_context.get("last_topic") if conversation_context else None
            prev_text = conversation_context.get("last_text") if conversation_context else None
            return self._handle_simplification(prev_topic, prev_text)

        # 2. Check for Specific High-Frequency Clinical Questions
        # A. Sleep inquiry
        if intent == "sleep_health" or any(w in query_lower for w in ["sleep", "insomnia", "sleepless", "awake all night", "can't sleep"]):
            return self._handle_sleep_inquiry(query)

        # B. Stomach / abdominal pain
        if intent == "stomach_digestive" or any(w in query_lower for w in ["stomach", "tummy", "belly", "abdomen", "gastritis", "acid reflux", "indigestion"]):
            return self._handle_stomach_pain_inquiry(query)

        # C. Hemoglobin / Iron
        if any(w in query_lower for w in ["hemoglobin", "haemoglobin", "iron", "low hb", "anemia"]):
            return self._handle_hemoglobin_inquiry(query)

        # D. Virus vs bacteria
        if ("virus" in query_lower and "bacteria" in query_lower) or "difference between virus" in query_lower:
            return self._handle_virus_vs_bacteria(query)

        # 3. Knowledge Base Match
        if matched_record and (similarity_score >= 0.12 or entities.get("conditions") or entities.get("symptoms")):
            topic = matched_record.get('topic', '')
            category = matched_record.get('category', '')
            desc = matched_record.get('description', '')
            symptoms = matched_record.get('symptoms', [])
            causes = matched_record.get('causes', '')
            prevention = matched_record.get('prevention', '')
            when_to_seek = matched_record.get('when_to_seek_care', '')
            refs = matched_record.get('references', [])

            symptoms_list_md = "\n".join([f"• {s}" for s in symptoms]) if isinstance(symptoms, list) else f"• {symptoms}"

            if intent == "symptom_inquiry":
                response = (
                    f"### 📋 Symptoms & Characteristics of {topic}\n\n"
                    f"**Category:** {category}\n\n"
                    f"{desc}\n\n"
                    f"**Common Associated Symptoms:**\n{symptoms_list_md}\n\n"
                    f"**⚠️ When to Seek Medical Attention:**\n{when_to_seek}\n\n"
                    f"**Potential Causes & Triggers:** {causes}"
                )
            elif intent == "cause_inquiry":
                response = (
                    f"### 🔍 Causes & Triggers of {topic}\n\n"
                    f"**Overview:** {desc}\n\n"
                    f"**Underlying Causes & Risk Factors:**\n{causes}\n\n"
                    f"**Prevention Guidance:**\n{prevention}\n\n"
                    f"**Common Associated Symptoms:**\n{symptoms_list_md}"
                )
            elif intent == "prevention_inquiry":
                response = (
                    f"### 🛡️ Prevention & Risk Reduction for {topic}\n\n"
                    f"**Preventive Steps & Healthy Habits:**\n{prevention}\n\n"
                    f"**Why Prevention Matters:** {desc}\n\n"
                    f"**Associated Triggers to Avoid:**\n{causes}"
                )
            elif intent == "treatment_caution":
                response = (
                    f"### 💊 General Management & Care for {topic}\n\n"
                    f"**Educational Overview:** {desc}\n\n"
                    f"**Supportive Self-Care Measures:**\n{prevention}\n\n"
                    f"**⚠️ Warning Signs & Clinical Evaluation:**\n{when_to_seek}\n\n"
                    f"*Clinical Note: Actual medication regimens and therapies must be prescribed by a licensed healthcare provider.*"
                )
            else:
                response = (
                    f"### 🩺 Educational Guide: {topic}\n\n"
                    f"**Category:** {category}\n\n"
                    f"{desc}\n\n"
                    f"**Common Symptoms:**\n{symptoms_list_md}\n\n"
                    f"**Causes & Risk Factors:**\n{causes}\n\n"
                    f"**Prevention & Lifestyle Recommendations:**\n{prevention}\n\n"
                    f"**⚠️ Warning Signs:**\n{when_to_seek}"
                )

            if refs:
                response += "\n\n**Reliable Sources & References:**\n"
                for r in refs:
                    response += f"- [{r.get('source')} - {r.get('title')}]({r.get('url')})\n"

            response += STANDARD_DISCLAIMER

            suggested = [
                f"What causes {topic}?",
                f"How to prevent {topic}?",
                f"When should I see a doctor for {topic}?",
                "What are healthy lifestyle habits?"
            ]
            return response, suggested

        # 4. If Symptoms were extracted from the query
        if entities.get("symptoms"):
            symptoms_found = ", ".join(entities["symptoms"])
            response = (
                f"### 🩺 Symptom Information Summary\n\n"
                f"You mentioned experiencing or asking about: **{symptoms_found}**.\n\n"
                f"**Clinical Context:**\n"
                f"Symptoms such as {symptoms_found} can arise from temporary lifestyle factors, benign viral illnesses, or underlying metabolic or muscular conditions. "
                f"Because symptoms often overlap across multiple diagnoses, a qualified physician's evaluation is recommended for an accurate assessment.\n\n"
                f"**General Supportive Care Steps:**\n"
                f"• Rest adequately and keep yourself well hydrated with clean fluids.\n"
                f"• Track the timing, severity, and any triggers that make the symptoms better or worse.\n"
                f"• Avoid strenuous physical exertion if feeling lightheaded or weak.\n\n"
                f"**⚠️ Warning Signs:** If symptoms become severe, persist beyond 48–72 hours, or include high fever, severe breathlessness, or sharp discomfort, seek immediate medical care."
            )
            response += STANDARD_DISCLAIMER
            suggested = [
                "What are warning signs of dehydration?",
                "What causes tension headaches?",
                "When to see a doctor for fever?",
                "How to maintain a healthy lifestyle?"
            ]
            return response, suggested

        # 5. Intelligent Scope-Guided Response (Zero Generic Fallback!)
        # Instead of static robotic list, analyze what the user is asking and give clear guidance
        response = (
            f"### 💡 Health Information Guidance\n\n"
            f"I hear your question regarding **'{query.strip()}'**.\n\n"
            f"As an AI healthcare assistant, I can provide evidence-based insights across multiple areas:\n"
            f"• **Common Symptoms:** Fever, headaches, coughs, stomach pain, fatigue, joint stiffness, and dizziness.\n"
            f"• **Medical Conditions:** Diabetes, hypertension, asthma, anemia, thyroid health, and heart wellness.\n"
            f"• **Sleep & Wellness:** Sleep hygiene, stress management, balanced diets, protein intake, and exercise.\n"
            f"• **Health Education:** Human body systems, first aid protocols, and differences between viruses and bacteria.\n\n"
            f"Could you tell me a little more about what specific symptoms, conditions, or wellness goals you are interested in?"
        )
        response += STANDARD_DISCLAIMER
        suggested = [
            "What causes sleeplessness?",
            "What is hypertension?",
            "How to increase hemoglobin?",
            "What is a balanced diet?"
        ]
        return response, suggested
