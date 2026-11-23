from rest_framework import views, status, permissions
from rest_framework.response import Response
from .models import Feedback
from .serializers import FeedbackSerializer
from analytics.models import ChatbotAnalytics

class FeedbackCreateView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else None
            fb = serializer.save(user=user)
            
            # Record feedback in analytics
            ChatbotAnalytics.record_feedback(is_helpful=fb.is_helpful, rating=fb.rating)
            
            return Response(FeedbackSerializer(fb).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedbackListView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        feedbacks = Feedback.objects.all()[:50]
        return Response(FeedbackSerializer(feedbacks, many=True).data)
