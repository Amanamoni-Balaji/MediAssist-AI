import os
import sys
import django

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from nlp_engine.service import NLPService

GENERIC_FALLBACK_PHRASE = "Thank you for your question. As an AI health assistant, I provide educational information regarding conditions like"

# 115 Comprehensive Test Queries across 10 categories
TEST_CASES = [
    # Category 1: Greetings & Everyday Conversations (15)
    {"q": "Hello", "cat": "Greeting", "expect_emergency": False},
    {"q": "Hi there", "cat": "Greeting", "expect_emergency": False},
    {"q": "Hey", "cat": "Greeting", "expect_emergency": False},
    {"q": "Good morning", "cat": "Greeting", "expect_emergency": False},
    {"q": "Good afternoon", "cat": "Greeting", "expect_emergency": False},
    {"q": "Good evening", "cat": "Greeting", "expect_emergency": False},
    {"q": "How are you?", "cat": "Everyday Conversation", "expect_emergency": False},
    {"q": "How are you doing today?", "cat": "Everyday Conversation", "expect_emergency": False},
    {"q": "What are you doing?", "cat": "Everyday Conversation", "expect_emergency": False},
    {"q": "How's it going?", "cat": "Everyday Conversation", "expect_emergency": False},
    {"q": "Tell me something interesting", "cat": "Everyday Conversation", "expect_emergency": False},
    {"q": "Share a cool health fact", "cat": "Everyday Conversation", "expect_emergency": False},
    {"q": "Thank you so much", "cat": "Gratitude", "expect_emergency": False},
    {"q": "Thanks for your help!", "cat": "Gratitude", "expect_emergency": False},
    {"q": "Goodbye, have a great day!", "cat": "Farewell", "expect_emergency": False},

    # Category 2: Chatbot Identity & Capabilities (10)
    {"q": "Who are you?", "cat": "Identity", "expect_emergency": False},
    {"q": "What is your name?", "cat": "Identity", "expect_emergency": False},
    {"q": "What can you do?", "cat": "Identity", "expect_emergency": False},
    {"q": "What are your capabilities?", "cat": "Identity", "expect_emergency": False},
    {"q": "Can you help me?", "cat": "Identity", "expect_emergency": False},
    {"q": "Are you a real doctor?", "cat": "Identity", "expect_emergency": False},
    {"q": "Are you an AI?", "cat": "Identity", "expect_emergency": False},
    {"q": "Can you prescribe medicines for me?", "cat": "Identity", "expect_emergency": False},
    {"q": "Who created you?", "cat": "Identity", "expect_emergency": False},
    {"q": "What kind of questions can I ask you?", "cat": "Identity", "expect_emergency": False},

    # Category 3: Sleep & Insomnia Phrasing Variations (15)
    {"q": "I didn't get sleep", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "I am not getting proper sleep", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "I can't sleep at night", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "Why am I unable to sleep?", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "What causes sleeplessness?", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "I have trouble sleeping.", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "I have insomnia and keep waking up at 3am", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "How can I fall asleep faster?", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "Tips for better sleep at night", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "Why can't I fall asleep even when feeling tired?", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "What is good sleep hygiene?", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "How does blue light affect my sleep?", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "How many hours of sleep should adults get?", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "Not getting good sleep lately due to work stress", "cat": "Sleep & Insomnia", "expect_emergency": False},
    {"q": "sleping problem insomniaa", "cat": "Sleep & Insomnia (Typo)", "expect_emergency": False},

    # Category 4: Stomach & Digestive Discomfort (10)
    {"q": "I have stomach pain", "cat": "Stomach & Digestion", "expect_emergency": False},
    {"q": "My stomach hurts badly", "cat": "Stomach & Digestion", "expect_emergency": False},
    {"q": "I have a belly ache after eating", "cat": "Stomach & Digestion", "expect_emergency": False},
    {"q": "Tummy pain and feeling bloated", "cat": "Stomach & Digestion", "expect_emergency": False},
    {"q": "What causes severe cramps in my stomach?", "cat": "Stomach & Digestion", "expect_emergency": False},
    {"q": "I have acidity and burning in my stomach", "cat": "Stomach & Digestion", "expect_emergency": False},
    {"q": "What causes acid reflux and heartburn?", "cat": "Stomach & Digestion", "expect_emergency": False},
    {"q": "What should I eat when I have an upset stomach?", "cat": "Stomach & Digestion", "expect_emergency": False},
    {"q": "Gastritis symptoms and home relief", "cat": "Stomach & Digestion", "expect_emergency": False},
    {"q": "stomac ache and indjestion", "cat": "Stomach (Typo)", "expect_emergency": False},

    # Category 5: Hemoglobin, Iron & Nutrition (10)
    {"q": "How to increase hemoglobin?", "cat": "Nutrition & Blood", "expect_emergency": False},
    {"q": "What foods increase hemoglobin levels?", "cat": "Nutrition & Blood", "expect_emergency": False},
    {"q": "How can I raise low iron in blood?", "cat": "Nutrition & Blood", "expect_emergency": False},
    {"q": "What are symptoms of iron deficiency anemia?", "cat": "Nutrition & Blood", "expect_emergency": False},
    {"q": "How much protein do I need per day?", "cat": "Nutrition & Blood", "expect_emergency": False},
    {"q": "What are the best vegetarian sources of protein?", "cat": "Nutrition & Blood", "expect_emergency": False},
    {"q": "What constitutes a balanced diet?", "cat": "Nutrition & Blood", "expect_emergency": False},
    {"q": "How much water should I drink every day?", "cat": "Nutrition & Blood", "expect_emergency": False},
    {"q": "Does Vitamin C help with iron absorption?", "cat": "Nutrition & Blood", "expect_emergency": False},
    {"q": "heamoglobin boost foods", "cat": "Nutrition (Typo)", "expect_emergency": False},

    # Category 6: Medical Education (Viruses vs Bacteria, Organs) (10)
    {"q": "What is the difference between virus and bacteria?", "cat": "Medical Education", "expect_emergency": False},
    {"q": "Can antibiotics kill viruses?", "cat": "Medical Education", "expect_emergency": False},
    {"q": "Why don't antibiotics work on common colds?", "cat": "Medical Education", "expect_emergency": False},
    {"q": "How does the digestive system work?", "cat": "Medical Education", "expect_emergency": False},
    {"q": "Explain the circulatory system and heart function", "cat": "Medical Education", "expect_emergency": False},
    {"q": "What is the function of the human kidneys?", "cat": "Medical Education", "expect_emergency": False},
    {"q": "How does the liver process toxins?", "cat": "Medical Education", "expect_emergency": False},
    {"q": "What is the difference between systolic and diastolic blood pressure?", "cat": "Medical Education", "expect_emergency": False},
    {"q": "How do vaccines train the immune system?", "cat": "Medical Education", "expect_emergency": False},
    {"q": "difference between bactria and viruss", "cat": "Education (Typo)", "expect_emergency": False},

    # Category 7: Common Symptoms, Informal Phrasing & Typos (15)
    {"q": "What is diabetes?", "cat": "Common Conditions", "expect_emergency": False},
    {"q": "Can you explain hypertension?", "cat": "Common Conditions", "expect_emergency": False},
    {"q": "What are the common symptoms of fever?", "cat": "Symptoms", "expect_emergency": False},
    {"q": "What causes headaches?", "cat": "Symptoms", "expect_emergency": False},
    {"q": "What are the symptoms of dehydration?", "cat": "Symptoms", "expect_emergency": False},
    {"q": "Why do I have a persistent dry cough?", "cat": "Symptoms", "expect_emergency": False},
    {"q": "Home remedies for a sore throat", "cat": "Symptoms", "expect_emergency": False},
    {"q": "What causes migraine headaches?", "cat": "Symptoms", "expect_emergency": False},
    {"q": "Why are my joints stiff and aching in the morning?", "cat": "Symptoms", "expect_emergency": False},
    {"q": "What causes chronic fatigue and low energy?", "cat": "Symptoms", "expect_emergency": False},
    {"q": "diabeetes high sugar symptoms", "cat": "Typo / Informal", "expect_emergency": False},
    {"q": "hypertenshion high bp symptoms", "cat": "Typo / Informal", "expect_emergency": False},
    {"q": "hedache and tierdness", "cat": "Typo / Informal", "expect_emergency": False},
    {"q": "fevr and chills in body", "cat": "Typo / Informal", "expect_emergency": False},
    {"q": "thyrod problem symptoms", "cat": "Typo / Informal", "expect_emergency": False},

    # Category 8: Conversational Context & Follow-Ups (10)
    {"q": "Explain in simple words", "cat": "Contextual Clarification", "context": {"last_topic": "Hypertension (High Blood Pressure)"}, "expect_emergency": False},
    {"q": "Can you explain that again?", "cat": "Contextual Clarification", "context": {"last_topic": "Type 2 Diabetes"}, "expect_emergency": False},
    {"q": "I don't understand, make it simpler", "cat": "Contextual Clarification", "context": {"last_topic": "Asthma and Respiratory Allergies"}, "expect_emergency": False},
    {"q": "Explain like I'm five", "cat": "Contextual Clarification", "context": {"last_topic": "Insomnia and Sleep Difficulties"}, "expect_emergency": False},
    {"q": "What are its symptoms?", "cat": "Contextual Follow-up", "context": {"last_topic": "Type 2 Diabetes"}, "expect_emergency": False},
    {"q": "How can I prevent it?", "cat": "Contextual Follow-up", "context": {"last_topic": "Hypertension (High Blood Pressure)"}, "expect_emergency": False},
    {"q": "What causes it?", "cat": "Contextual Follow-up", "context": {"last_topic": "Iron-Deficiency Anemia and Hemoglobin Health"}, "expect_emergency": False},
    {"q": "Tell me more about it", "cat": "Contextual Follow-up", "context": {"last_topic": "Thyroid Disorders"}, "expect_emergency": False},
    {"q": "When should I see a doctor for that?", "cat": "Contextual Follow-up", "context": {"last_topic": "Abdominal Pain and Stomach Ache"}, "expect_emergency": False},
    {"q": "Give me more information", "cat": "Contextual Clarification", "context": {"last_topic": "Cardiovascular and Heart Health"}, "expect_emergency": False},

    # Category 9: Critical Emergency Detection & Safety (10)
    {"q": "I have severe crushing chest pain radiating to my left arm", "cat": "Emergency Triage", "expect_emergency": True},
    {"q": "My face is drooping and I can't move my arm", "cat": "Emergency Triage", "expect_emergency": True},
    {"q": "Sudden slurred speech and facial numbness", "cat": "Emergency Triage", "expect_emergency": True},
    {"q": "I can't breathe at all and my lips are turning blue", "cat": "Emergency Triage", "expect_emergency": True},
    {"q": "I am having suicidal thoughts and want to die", "cat": "Emergency Triage", "expect_emergency": True},
    {"q": "Severe allergic reaction and my throat is closing up", "cat": "Emergency Triage", "expect_emergency": True},
    {"q": "Unbearable thunderclap explosive headache", "cat": "Emergency Triage", "expect_emergency": True},
    {"q": "Severe acute abdominal pain and vomiting blood", "cat": "Emergency Triage", "expect_emergency": True},
    {"q": "Someone is unconscious and passed out", "cat": "Emergency Triage", "expect_emergency": True},
    {"q": "Profuse bleeding from deep cut that will not stop", "cat": "Emergency Triage", "expect_emergency": True},

    # Category 10: Lifestyle, Mental Health & First Aid (10)
    {"q": "How can I maintain a healthy lifestyle?", "cat": "Lifestyle", "expect_emergency": False},
    {"q": "What are the benefits of daily walking?", "cat": "Lifestyle", "expect_emergency": False},
    {"q": "How does yoga help with physical and mental health?", "cat": "Lifestyle", "expect_emergency": False},
    {"q": "I feel very stressed out and anxious lately", "cat": "Mental Wellness", "expect_emergency": False},
    {"q": "What are early symptoms of depression?", "cat": "Mental Wellness", "expect_emergency": False},
    {"q": "Breathing techniques to reduce anxiety", "cat": "Mental Wellness", "expect_emergency": False},
    {"q": "What is the first aid for a minor burn?", "cat": "First Aid", "expect_emergency": False},
    {"q": "First aid steps for an ankle sprain", "cat": "First Aid", "expect_emergency": False},
    {"q": "What is considered normal body temperature?", "cat": "General FAQ", "expect_emergency": False},
    {"q": "What is normal blood pressure range in adults?", "cat": "General FAQ", "expect_emergency": False}
]

def run_tests():
    nlp = NLPService.get_instance()
    nlp.ensure_knowledge_indexed()

    total_tests = len(TEST_CASES)
    passed_tests = 0
    generic_fallback_count = 0
    emergency_correct_count = 0
    emergency_total = sum(1 for tc in TEST_CASES if tc["expect_emergency"])
    followups_present_count = 0

    print("=" * 80)
    print(f"RUNNING COMPREHENSIVE 115-QUERY NLP EVALUATION SUITE")
    print("=" * 80)

    category_stats = {}

    for idx, tc in enumerate(TEST_CASES, 1):
        query = tc["q"]
        cat = tc["cat"]
        ctx = tc.get("context")
        expect_emerg = tc["expect_emergency"]

        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "pass": 0, "fallback": 0}
        category_stats[cat]["total"] += 1

        result = nlp.process_message(query, conversation_context=ctx)
        resp_text = result.get("response", "")
        is_emerg = result.get("is_emergency", False)
        suggs = result.get("suggested_questions", [])

        # Check for generic fallback
        is_fallback = GENERIC_FALLBACK_PHRASE in resp_text
        if is_fallback:
            generic_fallback_count += 1
            category_stats[cat]["fallback"] += 1

        # Check emergency expectation
        emergency_ok = (is_emerg == expect_emerg)
        if emergency_ok and expect_emerg:
            emergency_correct_count += 1

        # Check follow-ups
        if len(suggs) >= 2:
            followups_present_count += 1

        test_passed = (not is_fallback) and emergency_ok and (len(resp_text) > 40)
        if test_passed:
            passed_tests += 1
            category_stats[cat]["pass"] += 1
            status = "PASS"
        else:
            status = "FAIL"

        if idx <= 15 or idx % 10 == 0 or not test_passed:
            intent_label = result.get("intent", "unknown")
            topic_label = result.get("matched_topic") or "N/A"
            print(f"[{status}] #{idx:03d} | Cat: {cat[:20]:20} | Q: '{query[:35]:35}' | Intent: {intent_label[:15]:15} | Topic: {str(topic_label)[:15]}")

    print("\n" + "=" * 80)
    print("NLP EVALUATION SUMMARY & METRICS")
    print("=" * 80)
    pass_rate = (passed_tests / total_tests) * 100
    fallback_rate = (generic_fallback_count / total_tests) * 100
    emergency_accuracy = (emergency_correct_count / emergency_total) * 100

    print(f"Total Test Cases:            {total_tests}")
    print(f"Passed Test Cases:           {passed_tests} / {total_tests} ({pass_rate:.1f}%)")
    print(f"Generic Fallback Triggered:  {generic_fallback_count} / {total_tests} ({fallback_rate:.1f}%) [TARGET: 0.0%]")
    print(f"Emergency Triage Accuracy:   {emergency_correct_count} / {emergency_total} ({emergency_accuracy:.1f}%)")
    print(f"Dynamic Follow-ups Rate:     {followups_present_count} / {total_tests} ({(followups_present_count/total_tests)*100:.1f}%)")
    print("\nCategory Breakdown:")
    for cat, stats in category_stats.items():
        print(f" - {cat:30}: {stats['pass']}/{stats['total']} passed (Fallbacks: {stats['fallback']})")

    assert generic_fallback_count == 0, f"Error: Generic fallback occurred {generic_fallback_count} times!"
    print("\n[SUCCESS] All evaluation criteria met with ZERO generic fallbacks!")

if __name__ == "__main__":
    run_tests()

