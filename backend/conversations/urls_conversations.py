from django.urls import path
from .views import (
    ConversationListView,
    ConversationDetailView,
    ClearConversationView,
)

urlpatterns = [
    path('', ConversationListView.as_view(), name='conversations_root'),
    path('<uuid:pk>/', ConversationDetailView.as_view(), name='conversations_detail'),
    path('<uuid:pk>/clear/', ClearConversationView.as_view(), name='conversations_clear'),
]

