from django.urls import path
from .views import (
    ConversationListView,
    ConversationDetailView,
    ClearConversationView,
    SendMessageView
)

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversation_list'),
    path('conversations/<uuid:pk>/', ConversationDetailView.as_view(), name='conversation_detail'),
    path('conversations/<uuid:pk>/clear/', ClearConversationView.as_view(), name='conversation_clear'),
    path('chat/send/', SendMessageView.as_view(), name='chat_send'),
]

