from django.urls import path
from .views import ChatbotInfoView, SendMessageView

urlpatterns = [
    path('', ChatbotInfoView.as_view(), name='chatbot_root'),
    path('send/', SendMessageView.as_view(), name='chatbot_send'),
    path('chat/send/', SendMessageView.as_view(), name='chatbot_chat_send'),
]

