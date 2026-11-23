from django.contrib import admin
from django.urls import path, include
from .views import backend_welcome_view, api_root_view

urlpatterns = [
    # Root welcome & documentation page
    path('', backend_welcome_view, name='backend_welcome'),

    # API Root navigation
    path('api/', api_root_view, name='api_root'),

    # Django Admin console
    path('admin/', admin.site.urls),

    # Application API routes
    path('api/auth/', include('accounts.urls')),
    path('api/chatbot/', include('conversations.urls_chatbot')),
    path('api/conversations/', include('conversations.urls_conversations')),
    path('api/chat/', include('conversations.urls')),
    path('api/medical/', include('medical_knowledge.urls')),
    path('api/feedback/', include('feedback.urls')),
    path('api/analytics/', include('analytics.urls')),
]
