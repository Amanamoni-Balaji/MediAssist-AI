import os
import sys
import django

# Setup django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from medical_knowledge.models import MedicalKnowledge
from conversations.models import Conversation, ChatMessage
from analytics.models import ChatbotAnalytics
from feedback.models import Feedback

def run_system_verification():
    print("=" * 60)
    print("STARTING END-TO-END SYSTEM VERIFICATION")
    print("=" * 60)

    client = APIClient()

    # 1. Test Admin Login
    print("\n[1] Testing Admin Authentication...")
    login_res = client.post('/api/auth/login/', {
        'username': 'admin',
        'password': 'admin123'
    })
    assert login_res.status_code == 200, f"Login failed: {login_res.data}"
    token = login_res.data['access']
    print(f" -> Login successful! JWT Access token obtained: {token[:25]}...")
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # 2. Test User Profile Retrieval
    print("\n[2] Testing Profile Endpoint...")
    profile_res = client.get('/api/auth/profile/')
    assert profile_res.status_code == 200, f"Profile error: {profile_res.data}"
    print(f" -> Profile retrieved for user: {profile_res.data['username']} (Staff: {profile_res.data['is_staff']})")

    # 3. Test Medical Knowledge Topics
    print("\n[3] Testing Medical Knowledge Base...")
    topics_res = client.get('/api/medical/topics/')
    assert topics_res.status_code == 200, f"Topics error: {topics_res.data}"
    print(f" -> Total Medical Knowledge Topics in DB: {len(topics_res.data)}")
    for t in topics_res.data[:4]:
        print(f"    • {t['topic']} [{t['category']}] ({len(t['symptoms'])} symptoms, {len(t['references'])} references)")

    # 4. Test Symptom Analysis Endpoint
    print("\n[4] Testing Symptom Educational Assessment Tool...")
    symptom_res = client.post('/api/medical/symptoms/analyze/', {
        'symptoms': ['headache', 'fever', 'chills'],
        'free_text': 'I have had a high temperature and severe headache since yesterday.'
    }, format='json')
    assert symptom_res.status_code == 200, f"Symptom analyze error: {symptom_res.data}"
    data = symptom_res.data
    print(f" -> Input Symptoms: {data['input_symptoms']}")
    print(f" -> Emergency Flag: {data['is_emergency']}")
    print(f" -> Associated Conditions Found: {len(data['identified_conditions'])}")
    for cond in data['identified_conditions'][:2]:
        print(f"    - {cond['topic']} (Overlap score: {cond['overlap_score']}, Matching: {cond['matching_symptoms']})")

    # 5. Test AI Medical Chatbot NLP Pipeline Queries
    print("\n[5] Testing AI Medical Chatbot NLP Pipeline...")
    test_queries = [
        ("What is hypertension and how is it managed?", "Disease Info"),
        ("What are the common symptoms of fever?", "Symptom Inquiry"),
        ("How can I maintain a healthy lifestyle?", "Healthy Lifestyle"),
        ("I have severe crushing chest pain radiating to left arm and cannot breathe", "Emergency Alert"),
        ("Hello assistant, can you help me?", "Greeting")
    ]

    conv_id = None
    for q, label in test_queries:
        payload = {'message': q}
        if conv_id:
            payload['conversation_id'] = conv_id
        
        chat_res = client.post('/api/chat/chat/send/', payload, format='json')
        assert chat_res.status_code == 200, f"Chat error for '{q}': {chat_res.data}"
        cdata = chat_res.data
        conv_id = cdata['conversation_id']
        bot_msg = cdata['assistant_message']
        meta = cdata['nlp_metadata']

        print(f"\n -> Query [{label}]: \"{q}\"")
        print(f"    Intent: {meta['intent']} (Conf: {meta['confidence']})")
        print(f"    Emergency Flag: {meta['is_emergency']}")
        print(f"    Matched Topic: {meta['matched_topic']}")
        print(f"    Response Preview: {bot_msg['text'][:120]}...")

    # 6. Test Feedback Submission
    print("\n[6] Testing Feedback Module...")
    fb_res = client.post('/api/feedback/submit/', {
        'conversation': conv_id,
        'is_helpful': True,
        'rating': 5,
        'comment': 'Exceptional medical accuracy and clear disclaimer.'
    }, format='json')
    assert fb_res.status_code == 201, f"Feedback error: {fb_res.data}"
    print(f" -> Feedback submitted successfully: Rating {fb_res.data['rating']} stars.")

    # 7. Test Admin Analytics Dashboard
    print("\n[7] Testing Admin Dashboard Analytics...")
    admin_res = client.get('/api/analytics/dashboard/')
    assert admin_res.status_code == 200, f"Analytics error: {admin_res.data}"
    kpis = admin_res.data['kpis']
    print(f" -> KPIs Calculated:")
    print(f"    Total Users: {kpis['total_users']}")
    print(f"    Total Conversations: {kpis['total_conversations']}")
    print(f"    Total Queries: {kpis['total_queries']}")
    print(f"    Emergency Alerts: {kpis['emergency_alerts']}")
    print(f"    User Satisfaction: {kpis['satisfaction_percentage']}%")
    print(f"    ML Model Accuracy: {admin_res.data['ml_model_metrics'].get('accuracy')}")

    print("\n" + "=" * 60)
    print("ALL 7 CORE MODULES VERIFIED & WORKING PERFECTLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_system_verification()
