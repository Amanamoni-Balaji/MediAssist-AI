from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from medical_knowledge.models import MedicalKnowledge
from conversations.models import Conversation, ChatMessage

def backend_welcome_view(request):
    """
    Root view for http://127.0.0.1:8000/
    Renders a healthcare AI backend status dashboard in HTML,
    or returns JSON if requested by API clients.
    """
    if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
        return JsonResponse({
            "service": "MediNLP AI - Medical Healthcare Chatbot Backend",
            "version": "1.0.0",
            "status": "Operational",
            "documentation": "/api/",
            "admin": "/admin/",
            "endpoints": {
                "auth": "/api/auth/",
                "chatbot": "/api/chatbot/",
                "conversations": "/api/conversations/",
                "chat_pipeline": "/api/chat/",
                "medical_knowledge": "/api/medical/",
                "feedback": "/api/feedback/",
                "analytics": "/api/analytics/"
            }
        })

    # Query quick database stats for diagnostics
    total_users = User.objects.count()
    total_topics = MedicalKnowledge.objects.count()
    total_conversations = Conversation.objects.count()
    total_messages = ChatMessage.objects.count()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediNLP AI – Healthcare Backend Status</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
            line-height: 1.5;
            padding: 32px 16px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #0f172a 0%, #0369a1 100%);
            color: white;
            padding: 36px 32px;
            border-radius: 24px;
            box-shadow: 0 10px 25px -5px rgba(3, 105, 161, 0.2);
            margin-bottom: 24px;
        }}
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 12px;
            border: 1px solid rgba(52, 211, 153, 0.3);
        }}
        .badge-dot {{
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
        }}
        h1 {{ font-size: 28px; font-weight: 800; margin-bottom: 8px; }}
        .header p {{ color: #cbd5e1; font-size: 14px; max-width: 600px; }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            border-color: #0284c7;
        }}
        .card h3 {{ font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 4px; }}
        .card p {{ font-size: 12px; color: #64748b; margin-bottom: 12px; }}
        .card a {{
            display: inline-block;
            font-size: 12px;
            font-weight: 600;
            color: #0284c7;
            text-decoration: none;
        }}
        .card a:hover {{ text-decoration: underline; }}
        
        .stats {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 16px;
        }}
        .stat-pill {{
            background: rgba(255, 255, 255, 0.1);
            padding: 6px 14px;
            border-radius: 12px;
            font-size: 11px;
            color: #e2e8f0;
        }}
        .stat-pill strong {{ color: white; }}
        
        .footer {{
            text-align: center;
            font-size: 11px;
            color: #94a3b8;
            margin-top: 32px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="badge">
                <span class="badge-dot"></span>
                API Server Active & Healthy
            </div>
            <h1>MediNLP AI Backend Gateway</h1>
            <p>Django REST Framework, Natural Language Processing Engine, Machine Learning Intent Classifier, and Knowledge Retrieval Service.</p>
            
            <div class="stats">
                <div class="stat-pill">Database: <strong>Connected (SQLite)</strong></div>
                <div class="stat-pill">Clinical Topics: <strong>{total_topics} Verified (WHO/NHS)</strong></div>
                <div class="stat-pill">NLP Model: <strong>Calibrated LinearSVC</strong></div>
                <div class="stat-pill">Total Consultations: <strong>{total_conversations}</strong></div>
                <div class="stat-pill">Messages Processed: <strong>{total_messages}</strong></div>
            </div>
        </div>

        <h2 style="font-size: 18px; margin-bottom: 16px; color: #1e293b;">Primary API Endpoints</h2>
        <div class="grid">
            <div class="card">
                <h3>🩺 Medical Chatbot API</h3>
                <p>Natural language processing endpoint that classifies intent, extracts medical entities, and retrieves clinical guidance.</p>
                <a href="/api/chatbot/">Explore /api/chatbot/ &rarr;</a>
            </div>

            <div class="card">
                <h3>💬 Conversations & History</h3>
                <p>Manage patient consultation sessions, review prior chat history, and retrieve transcripts.</p>
                <a href="/api/conversations/">Explore /api/conversations/ &rarr;</a>
            </div>

            <div class="card">
                <h3>🔐 Authentication Service</h3>
                <p>User registration, JWT token generation, token refresh, and patient health profile management.</p>
                <a href="/api/auth/">Explore /api/auth/ &rarr;</a>
            </div>

            <div class="card">
                <h3>📚 Clinical Knowledge Base</h3>
                <p>14 verified healthcare topics, clinical symptom dictionary, and multi-symptom correlation analyzer.</p>
                <a href="/api/medical/topics/">Explore /api/medical/ &rarr;</a>
            </div>

            <div class="card">
                <h3>⭐ Patient Feedback</h3>
                <p>Review and submit 1–5 star ratings and clinical clarity feedback on AI responses.</p>
                <a href="/api/feedback/">Explore /api/feedback/ &rarr;</a>
            </div>

            <div class="card">
                <h3>📊 Administrative Analytics</h3>
                <p>Live KPIs, intent distributions, traffic trends, and genuine ML evaluation metrics.</p>
                <a href="/api/analytics/dashboard/">Explore /api/analytics/ &rarr;</a>
            </div>

            <div class="card">
                <h3>🛠️ Django Admin Panel</h3>
                <p>Comprehensive database management console for users, topics, chat messages, and analytics.</p>
                <a href="/admin/">Open /admin/ &rarr;</a>
            </div>

            <div class="card">
                <h3>⚛️ React Web Client</h3>
                <p>Modern responsive healthcare frontend application running on Vite.</p>
                <a href="http://localhost:5173" target="_blank">Open Frontend (http://localhost:5173) &rarr;</a>
            </div>
        </div>

        <div class="footer">
            MediNLP AI &copy; 2026 &bull; Educational Healthcare Information Assistant &bull; Not a Medical Diagnosis Tool
        </div>
    </div>
</body>
</html>"""
    return HttpResponse(html_content, content_type="text/html; charset=utf-8")


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root_view(request):
    """
    API root endpoint for http://127.0.0.1:8000/api/
    Returns navigation URLs for all available endpoints.
    """
    host = request.build_absolute_uri('/')[:-1]
    return Response({
        "message": "Welcome to the MediNLP AI Healthcare REST API",
        "documentation": f"{host}/",
        "admin_console": f"{host}/admin/",
        "endpoints": {
            "authentication": {
                "root": f"{host}/api/auth/",
                "register": f"{host}/api/auth/register/",
                "login": f"{host}/api/auth/login/",
                "refresh": f"{host}/api/auth/refresh/",
                "profile": f"{host}/api/auth/profile/",
                "change_password": f"{host}/api/auth/change-password/"
            },
            "chatbot": {
                "root": f"{host}/api/chatbot/",
                "send_message": f"{host}/api/chatbot/send/",
                "chat_pipeline": f"{host}/api/chat/chat/send/"
            },
            "conversations": {
                "root": f"{host}/api/conversations/",
                "list_and_create": f"{host}/api/conversations/",
                "detail_and_delete": f"{host}/api/conversations/<uuid:id>/",
                "clear_messages": f"{host}/api/conversations/<uuid:id>/clear/"
            },
            "medical_knowledge": {
                "root": f"{host}/api/medical/topics/",
                "topic_detail": f"{host}/api/medical/topics/<slug>/",
                "symptom_dictionary": f"{host}/api/medical/symptoms/dictionary/",
                "symptom_analyzer": f"{host}/api/medical/symptoms/analyze/"
            },
            "feedback": {
                "root": f"{host}/api/feedback/",
                "submit": f"{host}/api/feedback/submit/",
                "list": f"{host}/api/feedback/list/"
            },
            "analytics": {
                "root": f"{host}/api/analytics/dashboard/"
            }
        },
        "status": "Operational",
        "nlp_engine": {
            "model": "Calibrated LinearSVC",
            "feature_extraction": "TF-IDF (unigram-trigram)",
            "knowledge_base": "14 Topics (WHO, MedlinePlus, NHS)",
            "emergency_detector": "Active"
        }
    })

