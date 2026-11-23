import os
import sys
import uuid
import django

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from chatbot.service import ChatbotService
from conversation_context.context_manager import ContextManager

# 200 Diverse, Real-World Medical & Conversational Test Queries
TEST_QUERIES = [
    # --- DOMAIN 1: SKIN & DERMATOLOGY (25 queries) ---
    {"q": "My hands and feet sweat too much.", "cat": "Skin - Hyperhidrosis", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "I sweat too much even in winter", "cat": "Skin - Hyperhidrosis", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "My hands are always wet and dripping sweat", "cat": "Skin - Hyperhidrosis", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "My feet sweat excessively in shoes", "cat": "Skin - Hyperhidrosis", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "My palms become sweaty even when I am not doing anything", "cat": "Skin - Hyperhidrosis", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "Why do my hands and legs sweat so much?", "cat": "Skin - Hyperhidrosis", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "I experience excessive sweating", "cat": "Skin - Hyperhidrosis", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "I think I have hyperhidrosis", "cat": "Skin - Hyperhidrosis", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "My underarms sweat a lot through shirts", "cat": "Skin - Hyperhidrosis", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "i have sweat in hands", "cat": "Skin - Hyperhidrosis (Informal)", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "What treatments are available for hyperhidrosis?", "cat": "Skin - Hyperhidrosis", "expected_topic": "Hyperhidrosis", "expect_emergency": False},
    {"q": "What causes severe facial acne and pimples?", "cat": "Skin - Acne", "expected_topic": "Acne", "expect_emergency": False},
    {"q": "How to treat blackheads and oily skin breakouts?", "cat": "Skin - Acne", "expected_topic": "Acne", "expect_emergency": False},
    {"q": "Is benzoyl peroxide effective for whiteheads?", "cat": "Skin - Acne", "expected_topic": "Acne", "expect_emergency": False},
    {"q": "i have skin itching and red patches", "cat": "Skin - Eczema", "expected_topic": "Eczema", "expect_emergency": False},
    {"q": "What is atopic dermatitis flare?", "cat": "Skin - Eczema", "expected_topic": "Eczema", "expect_emergency": False},
    {"q": "How can I soothe dry itchy eczema on my elbows?", "cat": "Skin - Eczema", "expected_topic": "Eczema", "expect_emergency": False},
    {"q": "What causes silvery scaly skin patches on knees?", "cat": "Skin - Psoriasis", "expected_topic": "Psoriasis", "expect_emergency": False},
    {"q": "Is plaque psoriasis an autoimmune disorder?", "cat": "Skin - Psoriasis", "expected_topic": "Psoriasis", "expect_emergency": False},
    {"q": "why my hair falling so fast", "cat": "Skin - Hair Loss (Informal)", "expected_topic": "Hair", "expect_emergency": False},
    {"q": "What causes hair thinning in women?", "cat": "Skin - Hair Loss", "expected_topic": "Hair", "expect_emergency": False},
    {"q": "Can low ferritin or iron cause hair loss?", "cat": "Skin - Hair Loss", "expected_topic": "Hair", "expect_emergency": False},
    {"q": "How to treat athlete's foot peeling and itch?", "cat": "Skin - Fungal", "expected_topic": "Skin", "expect_emergency": False},
    {"q": "What causes ringworm fungal rash?", "cat": "Skin - Fungal", "expected_topic": "Skin", "expect_emergency": False},
    {"q": "How to manage very dry flaky winter skin?", "cat": "Skin - Dry Skin", "expected_topic": "Skin", "expect_emergency": False},

    # --- DOMAIN 2: GENERAL MEDICINE & COMMON SYMPTOMS (25 queries) ---
    {"q": "I have cold and cough.", "cat": "General Medicine", "expected_topic": "Cold", "expect_emergency": False},
    {"q": "What are the common symptoms of fever?", "cat": "General Medicine", "expected_topic": "Fever", "expect_emergency": False},
    {"q": "At what body temperature is a fever dangerous in adults?", "cat": "General Medicine", "expected_topic": "Fever", "expect_emergency": False},
    {"q": "fevr and chills with shivering", "cat": "General Medicine (Typo)", "expected_topic": "Fever", "expect_emergency": False},
    {"q": "my head is paining", "cat": "General Medicine (Informal)", "expected_topic": "Headache", "expect_emergency": False},
    {"q": "What causes severe tension headaches across temples?", "cat": "General Medicine", "expected_topic": "Headache", "expect_emergency": False},
    {"q": "hedache and tierdness from morning", "cat": "General Medicine (Typo)", "expected_topic": "Headache", "expect_emergency": False},
    {"q": "What triggers severe throbbing migraine with aura?", "cat": "General Medicine", "expected_topic": "Headache", "expect_emergency": False},
    {"q": "Why does bright light make my migraine worse?", "cat": "General Medicine", "expected_topic": "Headache", "expect_emergency": False},
    {"q": "Generalized muscle aches and body pain", "cat": "General Medicine", "expected_topic": None, "expect_emergency": False},
    {"q": "feeling weak from morning with zero energy", "cat": "General Medicine (Informal)", "expected_topic": "Fatigue", "expect_emergency": False},
    {"q": "What causes chronic fatigue syndrome?", "cat": "General Medicine", "expected_topic": "Fatigue", "expect_emergency": False},
    {"q": "Why do I feel dizzy when standing up quickly?", "cat": "General Medicine", "expected_topic": None, "expect_emergency": False},
    {"q": "What are common causes of vertigo and room spinning?", "cat": "General Medicine", "expected_topic": None, "expect_emergency": False},
    {"q": "How to manage nausea and vomiting at home?", "cat": "General Medicine", "expected_topic": None, "expect_emergency": False},
    {"q": "What should I drink during diarrhea and stomach flu?", "cat": "General Medicine", "expected_topic": None, "expect_emergency": False},
    {"q": "What are warning signs of dehydration in adults?", "cat": "General Medicine", "expected_topic": "Hydration", "expect_emergency": False},
    {"q": "Why does dehydration cause dark urine and dry mouth?", "cat": "General Medicine", "expected_topic": "Hydration", "expect_emergency": False},
    {"q": "How to soothe an itchy scratchy sore throat?", "cat": "General Medicine", "expected_topic": "Cold", "expect_emergency": False},
    {"q": "What are symptoms of seasonal airborne allergies?", "cat": "General Medicine", "expected_topic": "Asthma", "expect_emergency": False},
    {"q": "Can allergies cause watery eyes and sneezing?", "cat": "General Medicine", "expected_topic": "Cold", "expect_emergency": False},
    {"q": "Why are my hands shaking slightly?", "cat": "General Medicine (Informal)", "expected_topic": None, "expect_emergency": False},
    {"q": "my legs are swelling around ankles", "cat": "General Medicine (Informal)", "expected_topic": None, "expect_emergency": False},
    {"q": "What causes fluid retention and swollen feet?", "cat": "General Medicine", "expected_topic": None, "expect_emergency": False},
    {"q": "How to distinguish between cold and influenza flu?", "cat": "General Medicine", "expected_topic": "Cold", "expect_emergency": False},

    # --- DOMAIN 3: RESPIRATORY HEALTH (15 queries) ---
    {"q": "What is asthma and how does it restrict airways?", "cat": "Respiratory", "expected_topic": "Asthma", "expect_emergency": False},
    {"q": "getting breathing problem and wheezing", "cat": "Respiratory (Informal)", "expected_topic": "Asthma", "expect_emergency": False},
    {"q": "How does an albuterol inhaler work during asthma flare?", "cat": "Respiratory", "expected_topic": "Asthma", "expect_emergency": False},
    {"q": "What triggers nocturnal asthma cough at night?", "cat": "Respiratory", "expected_topic": "Asthma", "expect_emergency": False},
    {"q": "What is acute bronchitis and how long does it last?", "cat": "Respiratory", "expected_topic": "Bronchitis", "expect_emergency": False},
    {"q": "Why do antibiotics not work for acute viral bronchitis?", "cat": "Respiratory", "expected_topic": "Bronchitis", "expect_emergency": False},
    {"q": "Coughing up yellow green phlegm with chest tightness", "cat": "Respiratory", "expected_topic": "Bronchitis", "expect_emergency": False},
    {"q": "What are the common symptoms of pneumonia in adults?", "cat": "Respiratory", "expected_topic": "Bronchitis", "expect_emergency": False},
    {"q": "What causes severe sinus pressure behind my forehead?", "cat": "Respiratory", "expected_topic": "Headache", "expect_emergency": False},
    {"q": "How to clear blocked nasal sinuses naturally?", "cat": "Respiratory", "expected_topic": "Cold", "expect_emergency": False},
    {"q": "Can poor air quality and pollution trigger wheezing?", "cat": "Respiratory", "expected_topic": "Asthma", "expect_emergency": False},
    {"q": "Why does cold winter air cause airway bronchospasm?", "cat": "Respiratory", "expected_topic": "Asthma", "expect_emergency": False},
    {"q": "What is peak expiratory flow in asthma monitoring?", "cat": "Respiratory", "expected_topic": "Asthma", "expect_emergency": False},
    {"q": "Home steam inhalation for chest congestion", "cat": "Respiratory", "expected_topic": "Cold", "expect_emergency": False},
    {"q": "How does chronic smoking damage bronchial cilia?", "cat": "Respiratory", "expected_topic": "Bronchitis", "expect_emergency": False},

    # --- DOMAIN 4: CARDIOVASCULAR HEALTH (15 queries) ---
    {"q": "What is hypertension?", "cat": "Cardiovascular", "expected_topic": "Hypertension", "expect_emergency": False},
    {"q": "Can you explain high blood pressure?", "cat": "Cardiovascular", "expected_topic": "Hypertension", "expect_emergency": False},
    {"q": "What is normal blood pressure range in adults?", "cat": "Cardiovascular", "expected_topic": "Hypertension", "expect_emergency": False},
    {"q": "hypertenshion high bp symptoms", "cat": "Cardiovascular (Typo)", "expected_topic": "Hypertension", "expect_emergency": False},
    {"q": "What is the difference between systolic and diastolic pressure?", "cat": "Cardiovascular", "expected_topic": "Hypertension", "expect_emergency": False},
    {"q": "How does high dietary sodium intake elevate blood pressure?", "cat": "Cardiovascular", "expected_topic": "Hypertension", "expect_emergency": False},
    {"q": "What is the DASH diet for lowering hypertension?", "cat": "Cardiovascular", "expected_topic": "Hypertension", "expect_emergency": False},
    {"q": "What causes sudden low blood pressure hypotension?", "cat": "Cardiovascular", "expected_topic": "Hypertension", "expect_emergency": False},
    {"q": "Why do I feel lightheaded when standing up quickly?", "cat": "Cardiovascular", "expected_topic": "Hypertension", "expect_emergency": False},
    {"q": "What is coronary artery disease and arterial plaque?", "cat": "Cardiovascular", "expected_topic": "Cholesterol", "expect_emergency": False},
    {"q": "What is the difference between LDL and HDL cholesterol?", "cat": "Cardiovascular", "expected_topic": "Cholesterol", "expect_emergency": False},
    {"q": "How can diet lower high triglycerides and cholesterol?", "cat": "Cardiovascular", "expected_topic": "Cholesterol", "expect_emergency": False},
    {"q": "Why does my heart flutter or skip a beat palpitations?", "cat": "Cardiovascular", "expected_topic": None, "expect_emergency": False},
    {"q": "What are heart attack risk factors in adults?", "cat": "Cardiovascular", "expected_topic": "Cholesterol", "expect_emergency": False},
    {"q": "Benefits of daily aerobic cardio on arterial elasticity", "cat": "Cardiovascular", "expected_topic": "Exercise", "expect_emergency": False},

    # --- DOMAIN 5: ENDOCRINE & METABOLIC (15 queries) ---
    {"q": "What is type 2 diabetes?", "cat": "Endocrine", "expected_topic": "Diabetes", "expect_emergency": False},
    {"q": "What does insulin resistance mean in diabetes?", "cat": "Endocrine", "expected_topic": "Diabetes", "expect_emergency": False},
    {"q": "What are the common symptoms of diabetes?", "cat": "Endocrine", "expected_topic": "Diabetes", "expect_emergency": False},
    {"q": "Why does high blood sugar cause frequent urination and thirst?", "cat": "Endocrine", "expected_topic": "Diabetes", "expect_emergency": False},
    {"q": "What is HbA1c test and what does the percentage show?", "cat": "Endocrine", "expected_topic": "Diabetes", "expect_emergency": False},
    {"q": "diabeetes high sugar symptoms", "cat": "Endocrine (Typo)", "expected_topic": "Diabetes", "expect_emergency": False},
    {"q": "What are symptoms of hypothyroidism underactive thyroid?", "cat": "Endocrine", "expected_topic": "Thyroid", "expect_emergency": False},
    {"q": "thyrod problem symptoms", "cat": "Endocrine (Typo)", "expected_topic": "Thyroid", "expect_emergency": False},
    {"q": "What is the difference between hypothyroidism and hyperthyroidism?", "cat": "Endocrine", "expected_topic": "Thyroid", "expect_emergency": False},
    {"q": "Why does underactive thyroid cause cold intolerance and weight gain?", "cat": "Endocrine", "expected_topic": "Thyroid", "expect_emergency": False},
    {"q": "What is TSH blood test and what is normal range?", "cat": "Endocrine", "expected_topic": "Thyroid", "expect_emergency": False},
    {"q": "What is PCOS and what causes irregular cycles?", "cat": "Endocrine", "expected_topic": "PCOS", "expect_emergency": False},
    {"q": "How does insulin resistance contribute to PCOS symptoms?", "cat": "Endocrine", "expected_topic": "PCOS", "expect_emergency": False},
    {"q": "Can lifestyle changes help manage PCOS hormonal balance?", "cat": "Endocrine", "expected_topic": "PCOS", "expect_emergency": False},
    {"q": "What constitutes clinical obesity and visceral fat?", "cat": "Endocrine", "expected_topic": "Nutrition", "expect_emergency": False},

    # --- DOMAIN 6: MENTAL HEALTH & SLEEP (20 queries) ---
    {"q": "I cannot sleep properly.", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "I didn't get sleep", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "I am not getting proper sleep", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "I can't sleep at night", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "Why am I unable to sleep?", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "What causes sleeplessness?", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "I have trouble sleeping.", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "I keep waking up at 3am and cannot fall back asleep", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "not getting sleep lately due to work stress", "cat": "Mental - Sleep (Informal)", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "sleping problem insomniaa", "cat": "Mental - Sleep (Typo)", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "What is sleep hygiene and what are the best practices?", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "How does evening blue light from screens suppress melatonin?", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "How many hours of sleep should an adult get each night?", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "Why is bedroom temperature around 18-20C optimal for sleep?", "cat": "Mental - Sleep", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "How can I manage chronic stress effectively?", "cat": "Mental - Stress", "expected_topic": "Stress", "expect_emergency": False},
    {"q": "What physical symptoms does chronic anxiety cause?", "cat": "Mental - Anxiety", "expected_topic": "Stress", "expect_emergency": False},
    {"q": "Breathing techniques to calm a racing panic heart rate", "cat": "Mental - Anxiety", "expected_topic": "Stress", "expect_emergency": False},
    {"q": "What is the difference between everyday stress and clinical depression?", "cat": "Mental - Mood", "expected_topic": "Stress", "expect_emergency": False},
    {"q": "Signs of emotional burnout in workplace professionals", "cat": "Mental - Stress", "expected_topic": "Stress", "expect_emergency": False},
    {"q": "How does regular aerobic exercise metabolize cortisol?", "cat": "Mental - Wellness", "expected_topic": "Exercise", "expect_emergency": False},

    # --- DOMAIN 7: DIGESTIVE HEALTH (15 queries) ---
    {"q": "My stomach burns after eating.", "cat": "Digestive", "expected_topic": "Digestive", "expect_emergency": False},
    {"q": "stomach burning after food", "cat": "Digestive (Informal)", "expected_topic": "Digestive", "expect_emergency": False},
    {"q": "I have acidity and burning in my stomach", "cat": "Digestive", "expected_topic": "Digestive", "expect_emergency": False},
    {"q": "What causes gastroesophageal reflux disease GERD?", "cat": "Digestive", "expected_topic": "Digestive", "expect_emergency": False},
    {"q": "Why does lying down immediately after eating cause heartburn?", "cat": "Digestive", "expected_topic": "Digestive", "expect_emergency": False},
    {"q": "What foods trigger acid reflux episodes?", "cat": "Digestive", "expected_topic": "Digestive", "expect_emergency": False},
    {"q": "I have stomach pain", "cat": "Digestive", "expected_topic": "Abdominal", "expect_emergency": False},
    {"q": "My stomach hurts badly", "cat": "Digestive", "expected_topic": "Abdominal", "expect_emergency": False},
    {"q": "I have a belly ache after eating", "cat": "Digestive", "expected_topic": "Abdominal", "expect_emergency": False},
    {"q": "Tummy pain and feeling bloated", "cat": "Digestive", "expected_topic": "Abdominal", "expect_emergency": False},
    {"q": "stomac ache and indjestion", "cat": "Digestive (Typo)", "expected_topic": "Abdominal", "expect_emergency": False},
    {"q": "What is gastritis and what causes gastric mucosa irritation?", "cat": "Digestive", "expected_topic": "Digestive", "expect_emergency": False},
    {"q": "Why are NSAIDs like ibuprofen harmful on an empty stomach?", "cat": "Digestive", "expected_topic": "Abdominal", "expect_emergency": False},
    {"q": "What is non-alcoholic fatty liver disease?", "cat": "Digestive", "expected_topic": None, "expect_emergency": False},
    {"q": "What causes chronic constipation and hard stools?", "cat": "Digestive", "expected_topic": None, "expect_emergency": False},

    # --- DOMAIN 8: NUTRITION & LIFESTYLE (20 queries) ---
    {"q": "How to increase hemoglobin?", "cat": "Nutrition", "expected_topic": "Iron", "expect_emergency": False},
    {"q": "What foods increase hemoglobin levels?", "cat": "Nutrition", "expected_topic": "Iron", "expect_emergency": False},
    {"q": "How can I raise low iron in blood?", "cat": "Nutrition", "expected_topic": "Iron", "expect_emergency": False},
    {"q": "What are symptoms of iron deficiency anemia?", "cat": "Nutrition", "expected_topic": "Iron", "expect_emergency": False},
    {"q": "heamoglobin boost foods", "cat": "Nutrition (Typo)", "expected_topic": "Iron", "expect_emergency": False},
    {"q": "Why is Vitamin C paired with plant-based non-heme iron?", "cat": "Nutrition", "expected_topic": "Iron", "expect_emergency": False},
    {"q": "Why does drinking tea or coffee with meals block iron absorption?", "cat": "Nutrition", "expected_topic": "Iron", "expect_emergency": False},
    {"q": "How much protein do I need per day?", "cat": "Nutrition", "expected_topic": "Protein", "expect_emergency": False},
    {"q": "What are the best vegetarian sources of dietary protein?", "cat": "Nutrition", "expected_topic": "Protein", "expect_emergency": False},
    {"q": "Why is protein essential for muscle tissue repair?", "cat": "Nutrition", "expected_topic": "Protein", "expect_emergency": False},
    {"q": "What constitutes a balanced diet?", "cat": "Nutrition", "expected_topic": "Balanced", "expect_emergency": False},
    {"q": "What is the Eatwell plate recommendation?", "cat": "Nutrition", "expected_topic": "Balanced", "expect_emergency": False},
    {"q": "How many grams of dietary fiber should adults eat daily?", "cat": "Nutrition", "expected_topic": "Balanced", "expect_emergency": False},
    {"q": "Why are ultra-processed foods detrimental to long-term health?", "cat": "Nutrition", "expected_topic": "Balanced", "expect_emergency": False},
    {"q": "How much water should I drink every day?", "cat": "Nutrition", "expected_topic": "Balanced", "expect_emergency": False},
    {"q": "Why are electrolytes like sodium and potassium necessary?", "cat": "Nutrition", "expected_topic": "Balanced", "expect_emergency": False},
    {"q": "How can I maintain a healthy lifestyle?", "cat": "Lifestyle", "expected_topic": "Balanced", "expect_emergency": False},
    {"q": "What are the health benefits of 30 minutes of daily walking?", "cat": "Lifestyle", "expected_topic": "Balanced", "expect_emergency": False},
    {"q": "How much moderate aerobic exercise should an adult get weekly?", "cat": "Lifestyle", "expected_topic": "Hypertension", "expect_emergency": False},
    {"q": "What are common symptoms of Vitamin D deficiency?", "cat": "Nutrition", "expected_topic": "Balanced", "expect_emergency": False},

    # --- DOMAIN 9: MEDICAL EDUCATION & FIRST AID (15 queries) ---
    {"q": "What is the difference between bacteria and viruses?", "cat": "Education", "expected_topic": "Viruses", "expect_emergency": False},
    {"q": "What is the difference between virus and bacteria?", "cat": "Education", "expected_topic": "Viruses", "expect_emergency": False},
    {"q": "difference between bactria and viruss", "cat": "Education (Typo)", "expected_topic": "Viruses", "expect_emergency": False},
    {"q": "Can antibiotics kill viruses?", "cat": "Education", "expected_topic": "Viruses", "expect_emergency": False},
    {"q": "Why don't antibiotics work on common colds or flu?", "cat": "Education", "expected_topic": "Viruses", "expect_emergency": False},
    {"q": "What is global antibiotic resistance and why is it dangerous?", "cat": "Education", "expected_topic": "Viruses", "expect_emergency": False},
    {"q": "How do vaccines train the human immune system?", "cat": "Education", "expected_topic": "Viruses", "expect_emergency": False},
    {"q": "What are human body organ systems?", "cat": "Education", "expected_topic": None, "expect_emergency": False},
    {"q": "What is first aid for a minor thermal skin burn?", "cat": "First Aid", "expected_topic": "First Aid", "expect_emergency": False},
    {"q": "Why should you never put ice or butter on a fresh burn?", "cat": "First Aid", "expected_topic": "First Aid", "expect_emergency": False},
    {"q": "What is the RICE protocol for acute ankle sprains?", "cat": "First Aid", "expected_topic": "First Aid", "expect_emergency": False},
    {"q": "What is the proper first aid technique for a nosebleed?", "cat": "First Aid", "expected_topic": "First Aid", "expect_emergency": False},
    {"q": "Why should you lean forward during a nosebleed instead of backward?", "cat": "First Aid", "expected_topic": "First Aid", "expect_emergency": False},
    {"q": "What is the Heimlich maneuver for a choking conscious adult?", "cat": "First Aid", "expected_topic": "First Aid", "expect_emergency": False},
    {"q": "How to treat a bleeding laceration cut with direct pressure?", "cat": "First Aid", "expected_topic": "First Aid", "expect_emergency": False},

    # --- DOMAIN 10: CONVERSATIONAL & IDENTITY (15 queries) ---
    {"q": "Hello", "cat": "Greeting", "expected_topic": None, "expect_emergency": False},
    {"q": "Hi there", "cat": "Greeting", "expected_topic": None, "expect_emergency": False},
    {"q": "Hey", "cat": "Greeting", "expected_topic": None, "expect_emergency": False},
    {"q": "Good morning", "cat": "Greeting", "expected_topic": None, "expect_emergency": False},
    {"q": "Good afternoon", "cat": "Greeting", "expected_topic": None, "expect_emergency": False},
    {"q": "Good evening", "cat": "Greeting", "expected_topic": None, "expect_emergency": False},
    {"q": "How are you?", "cat": "Everyday Conversation", "expected_topic": None, "expect_emergency": False},
    {"q": "How are you doing today?", "cat": "Everyday Conversation", "expected_topic": None, "expect_emergency": False},
    {"q": "What are you doing?", "cat": "Everyday Conversation", "expected_topic": None, "expect_emergency": False},
    {"q": "Tell me something interesting", "cat": "Everyday Conversation", "expected_topic": None, "expect_emergency": False},
    {"q": "Who are you?", "cat": "Identity", "expected_topic": None, "expect_emergency": False},
    {"q": "What can you do?", "cat": "Identity", "expected_topic": None, "expect_emergency": False},
    {"q": "Can you help me?", "cat": "Identity", "expected_topic": None, "expect_emergency": False},
    {"q": "Thank you so much", "cat": "Gratitude", "expected_topic": None, "expect_emergency": False},
    {"q": "Goodbye, have a great day!", "cat": "Farewell", "expected_topic": None, "expect_emergency": False},

    # --- DOMAIN 11: CRITICAL EMERGENCY TRIAGE (15 queries) ---
    {"q": "My chest is hurting and I cannot breathe properly.", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "I have severe crushing chest pain radiating to my left arm", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "Crushing center chest pressure radiating to jaw and back", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "My face is drooping and I can't move my arm", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "Sudden slurred speech and facial paralysis on one side", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "I can't breathe at all and my lips are turning blue", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "Sudden acute shortness of breath and asphyxiation", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "Severe allergic reaction and my throat is closing up", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "Anaphylaxis attack and unable to swallow air", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "I am having suicidal thoughts and want to die", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "I want to harm myself and end my life", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "Coughing up a lot of blood continuously", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "Vomiting large amounts of blood and feeling faint", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "Unbearable explosive thunderclap headache worse than ever", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},
    {"q": "Deep arterial cut bleeding continuously and won't stop", "cat": "Emergency Triage", "expected_topic": "Emergency", "expect_emergency": True},

    # --- DOMAIN 12: UNKNOWN / BROAD SCOPE QUESTIONS (5 queries) ---
    {"q": "What should I know about rare metabolic enzymes?", "cat": "Broad / Unknown", "expected_topic": None, "expect_emergency": False},
    {"q": "Can you explain mitochondrial genetics simply?", "cat": "Broad / Unknown", "expected_topic": None, "expect_emergency": False},
    {"q": "What causes idiopathic peripheral neuropathy?", "cat": "Broad / Unknown", "expected_topic": None, "expect_emergency": False},
    {"q": "Tell me about uncommon sleep parasomnias", "cat": "Broad / Unknown", "expected_topic": "Insomnia", "expect_emergency": False},
    {"q": "How do telomeres influence cellular biological aging?", "cat": "Broad / Unknown", "expected_topic": None, "expect_emergency": False}
]

# MULTI-TURN CONVERSATION SCENARIOS SPECIFICALLY MANDATED BY USER
REQUIRED_CONVERSATIONS = [
    {
        "id": "TEST 1: Cold & Cough -> What can I take?",
        "turns": [
            {
                "user": "I have cold and cough.",
                "check": lambda r: "cold" in r["response"].lower() and not r["is_emergency"],
                "desc": "Provides relevant information about cold and cough"
            },
            {
                "user": "What can I take?",
                "check": lambda r: ("antibiotic" in r["response"].lower() or "paracetamol" in r["response"].lower() or "saline" in r["response"].lower() or "honey" in r["response"].lower()) and "doctor" in r["response"].lower(),
                "desc": "Understands previous context, provides safe general medication info, warns about antibiotics"
            }
        ]
    },
    {
        "id": "TEST 2: Excessive sweating -> How can I control it?",
        "turns": [
            {
                "user": "My hands and feet sweat too much.",
                "check": lambda r: "hyperhidrosis" in r["response"].lower() or "sweat" in r["response"].lower(),
                "desc": "Recognizes excessive sweating and explains hyperhidrosis"
            },
            {
                "user": "How can I control it?",
                "check": lambda r: ("antiperspirant" in r["response"].lower() or "iontophoresis" in r["response"].lower() or "socks" in r["response"].lower()) and "hyperhidrosis" in r["response"].lower(),
                "desc": "Understands previous context and explains management options for hyperhidrosis"
            }
        ]
    },
    {
        "id": "TEST 3: Cannot sleep properly -> What causes this?",
        "turns": [
            {
                "user": "I cannot sleep properly.",
                "check": lambda r: "sleep" in r["response"].lower() or "insomnia" in r["response"].lower(),
                "desc": "Provides relevant sleep information"
            },
            {
                "user": "What causes this?",
                "check": lambda r: ("screen" in r["response"].lower() or "caffeine" in r["response"].lower() or "stress" in r["response"].lower() or "melatonin" in r["response"].lower()) and ("sleep" in r["response"].lower() or "insomnia" in r["response"].lower()),
                "desc": "Understands user is referring to sleep difficulties causes"
            }
        ]
    },
    {
        "id": "TEST 4: Stomach burns after eating",
        "turns": [
            {
                "user": "My stomach burns after eating.",
                "check": lambda r: ("reflux" in r["response"].lower() or "acid" in r["response"].lower() or "gastritis" in r["response"].lower() or "heartburn" in r["response"].lower()) and not r["is_emergency"],
                "desc": "Provides relevant digestive health info and asks appropriate clarifying questions"
            }
        ]
    },
    {
        "id": "TEST 5: Bacteria vs Viruses",
        "turns": [
            {
                "user": "What is the difference between bacteria and viruses?",
                "check": lambda r: "antibiotic" in r["response"].lower() and "bacteria" in r["response"].lower() and "virus" in r["response"].lower(),
                "desc": "Provides an accurate educational comparison"
            }
        ]
    },
    {
        "id": "TEST 6: Chest is hurting and cannot breathe properly",
        "turns": [
            {
                "user": "My chest is hurting and I cannot breathe properly.",
                "check": lambda r: r["is_emergency"] is True and ("911" in r["response"] or "emergency" in r["response"].lower()),
                "desc": "Recognizes potential emergency symptoms and advises immediate emergency assistance"
            }
        ]
    }
]

GENERIC_FALLBACK_PHRASE = "Thank you for your question. As an AI health assistant, I provide educational information regarding conditions like"

def run_evaluation():
    service = ChatbotService.get_instance()
    service.rag_engine.ensure_indexed()

    print("=" * 80)
    print("RUNNING COMPLETE 200-QUERY AI MEDICAL CHATBOT EVALUATION SUITE")
    print("=" * 80)

    total_queries = len(TEST_QUERIES)
    passed_queries = 0
    fallback_count = 0
    emergency_correct = 0
    emergency_total = sum(1 for t in TEST_QUERIES if t["expect_emergency"])
    followups_present = 0

    category_stats = {}

    for idx, tc in enumerate(TEST_QUERIES, 1):
        q = tc["q"]
        cat = tc["cat"]
        expect_emerg = tc["expect_emergency"]
        expected_top = tc.get("expected_topic")

        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "pass": 0, "fallback": 0}
        category_stats[cat]["total"] += 1

        conv_id = f"test-eval-{idx}"
        res = service.process_user_message(q, conversation_id=conv_id)
        resp = res.get("response", "")
        is_emerg = res.get("is_emergency", False)
        suggs = res.get("suggested_questions", [])
        matched_topic = res.get("matched_topic") or ""

        # Check for robotic fallback
        is_fallback = GENERIC_FALLBACK_PHRASE in resp
        if is_fallback:
            fallback_count += 1
            category_stats[cat]["fallback"] += 1

        # Check emergency triage
        emerg_ok = (is_emerg == expect_emerg)
        if emerg_ok and expect_emerg:
            emergency_correct += 1

        # Check follow-ups
        if len(suggs) >= 2:
            followups_present += 1

        # Check topic alignment if specified
        topic_ok = True
        if expected_top:
            topic_ok = (expected_top.lower() in matched_topic.lower()) or (expected_top.lower() in resp.lower())

        test_passed = (not is_fallback) and emerg_ok and (len(resp) > 30) and topic_ok
        if test_passed:
            passed_queries += 1
            category_stats[cat]["pass"] += 1
            status = "PASS"
        else:
            status = "FAIL"

        if idx <= 15 or idx % 25 == 0 or not test_passed:
            print(f"[{status}] #{idx:03d} | Cat: {cat[:25]:25} | Q: '{q[:35]:35}' | Topic: {matched_topic[:20]:20} | Emerg: {is_emerg}")

    print("\n" + "=" * 80)
    print("RUNNING 6 SPECIFIC USER-MANDATED MULTI-TURN CONVERSATIONS")
    print("=" * 80)

    conv_pass_count = 0
    for conv in REQUIRED_CONVERSATIONS:
        cid = str(uuid.uuid4())
        c_id = conv["id"]
        print(f"\n--- {c_id} ---")
        all_turns_ok = True
        for t_idx, turn in enumerate(conv["turns"], 1):
            u_text = turn["user"]
            res = service.process_user_message(u_text, conversation_id=cid)
            turn_ok = turn["check"](res)
            print(f"Turn {t_idx} User: '{u_text}'")
            print(f"Turn {t_idx} Bot Topic: {res.get('matched_topic')} | Emerg: {res.get('is_emergency')} | Status: {'OK' if turn_ok else 'FAIL'}")
            print(f"Turn {t_idx} Snippet: {res['response'][:90].replace(chr(10), ' ')}...")
            if not turn_ok:
                all_turns_ok = False
        if all_turns_ok:
            conv_pass_count += 1
            print(f"Result for {c_id}: PASSED")
        else:
            print(f"Result for {c_id}: FAILED")

    print("\n" + "=" * 80)
    print("AI MEDICAL CHATBOT EVALUATION METRICS REPORT")
    print("=" * 80)
    query_pass_rate = (passed_queries / total_queries) * 100
    emergency_acc = (emergency_correct / emergency_total) * 100
    followup_rate = (followups_present / total_queries) * 100
    conv_pass_rate = (conv_pass_count / len(REQUIRED_CONVERSATIONS)) * 100

    print(f"Total Single Queries Evaluated:    {total_queries}")
    print(f"Passed Single Queries:             {passed_queries} / {total_queries} ({query_pass_rate:.1f}%)")
    print(f"Robotic Fallback Rate:             {fallback_count} / {total_queries} ({fallback_count/total_queries*100:.1f}%) [TARGET: 0.0%]")
    print(f"Emergency Detection Accuracy:      {emergency_correct} / {emergency_total} ({emergency_acc:.1f}%)")
    print(f"Follow-Up Suggestions Presence:    {followups_present} / {total_queries} ({followup_rate:.1f}%)")
    print(f"Mandated Multi-Turn Conversations: {conv_pass_count} / {len(REQUIRED_CONVERSATIONS)} ({conv_pass_rate:.1f}%)")
    print("\nDomain Performance Breakdown:")
    for cat, stats in category_stats.items():
        print(f" - {cat:35}: {stats['pass']}/{stats['total']} passed")

    assert fallback_count == 0, f"Error: Generic fallback occurred {fallback_count} times!"
    assert conv_pass_count == len(REQUIRED_CONVERSATIONS), "Error: Mandated multi-turn conversation failed!"
    print("\n[SUCCESS] Comprehensive 200-Query AI Healthcare Evaluation Passed Successfully!")

if __name__ == "__main__":
    run_evaluation()

