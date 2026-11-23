import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User

def test_all_routes():
    print("=" * 65)
    print("TESTING ALL DJANGO URL ROUTES AND API ENDPOINTS")
    print("=" * 65)

    client = APIClient()

    endpoints_to_test = [
        # (Method, URL, Payload, Expected Status Codes, Description)
        ('GET', '/', None, [200], 'Root Welcome Page'),
        ('GET', '/admin/', None, [200, 302], 'Django Admin Console'),
        ('GET', '/api/', None, [200], 'API Root Overview'),
        ('GET', '/api/auth/', None, [200], 'Auth Service Root'),
        ('POST', '/api/auth/login/', {'username': 'admin', 'password': 'admin123'}, [200], 'User JWT Login'),
        ('GET', '/api/chatbot/', None, [200], 'Medical Chatbot Info Root'),
        ('POST', '/api/chatbot/send/', {'message': 'What is asthma?'}, [200], 'Medical Chatbot Send (api/chatbot/send/)'),
        ('POST', '/api/chatbot/', {'message': 'What is diabetes?'}, [200], 'Medical Chatbot Send Direct (api/chatbot/)'),
        ('GET', '/api/conversations/', None, [200], 'Conversations History List'),
        ('GET', '/api/feedback/', None, [200], 'Feedback List Root'),
        ('POST', '/api/feedback/submit/', {'rating': 5, 'is_helpful': True, 'comment': 'Great'}, [201], 'Feedback Submit'),
        ('GET', '/api/medical/', None, [200], 'Medical Knowledge Root'),
        ('GET', '/api/medical/topics/', None, [200], 'Medical Topics List'),
        ('GET', '/api/analytics/', None, [200], 'Analytics Root'),
        ('GET', '/api/analytics/dashboard/', None, [200], 'Analytics Dashboard'),
        # Backward compatibility with React frontend
        ('POST', '/api/chat/chat/send/', {'message': 'Symptoms of fever'}, [200], 'React Frontend Chat Route'),
        ('GET', '/api/chat/conversations/', None, [200], 'React Frontend Conversations Route'),
    ]

    all_passed = True
    for method, path, payload, expected_statuses, desc in endpoints_to_test:
        if method == 'GET':
            res = client.get(path)
        else:
            res = client.post(path, payload, format='json')

        passed = res.status_code in expected_statuses
        status_str = f"PASS ({res.status_code})" if passed else f"FAIL ({res.status_code})"
        if not passed:
            all_passed = False

        print(f"[{status_str:10}] {method:4} {path:30} -> {desc}")

    print("=" * 65)
    if all_passed:
        print("SUCCESS: ALL 17 ROUTES & ENDPOINTS RETURNED VALID HTTP RESPONSES!")
    else:
        print("FAILURE: Some routes did not return expected status codes.")
    print("=" * 65)
    return all_passed

if __name__ == '__main__':
    success = test_all_routes()
    sys.exit(0 if success else 1)

