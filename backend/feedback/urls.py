from django.urls import path
from .views import FeedbackCreateView, FeedbackListView

urlpatterns = [
    path('', FeedbackListView.as_view(), name='feedback_root'),
    path('submit/', FeedbackCreateView.as_view(), name='feedback_submit'),
    path('list/', FeedbackListView.as_view(), name='feedback_list'),
]

