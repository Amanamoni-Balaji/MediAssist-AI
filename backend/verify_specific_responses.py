import os
import sys
import django

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from nlp_engine.service import NLPService

nlp = NLPService.get_instance()
nlp.ensure_knowledge_indexed()

test_queries = [
    ("I didn't get sleep", None),
    ("I have stomach pain", None),
    ("How to increase hemoglobin?", None),
    ("What is the difference between virus and bacteria?", None),
    ("How are you?", None),
    ("Who are you?", None),
    ("Explain in simple words", {"last_topic": "Hypertension (High Blood Pressure)"})
]

for q, ctx in test_queries:
    print("\n" + "=" * 70)
    print(f"USER QUERY: {q}")
    if ctx:
        print(f"CONTEXT: {ctx}")
    print("-" * 70)
    res = nlp.process_message(q, conversation_context=ctx)
    print(f"Intent: {res['intent']} | Topic: {res.get('matched_topic')}")
    print(f"Follow-ups: {res['suggested_questions']}")
    print("-" * 70)
    print(res['response'])

