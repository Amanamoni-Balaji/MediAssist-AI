from django.urls import path
from .views import AdminDashboardAnalyticsView

urlpatterns = [
    path('', AdminDashboardAnalyticsView.as_view(), name='analytics_root'),
    path('dashboard/', AdminDashboardAnalyticsView.as_view(), name='admin_dashboard_analytics'),
]

