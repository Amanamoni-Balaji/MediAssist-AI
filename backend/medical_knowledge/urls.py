from django.urls import path
from .views import (
    MedicalKnowledgeListView,
    MedicalKnowledgeDetailView,
    SymptomDictionaryView,
    SymptomAnalyzerView
)

urlpatterns = [
    path('', MedicalKnowledgeListView.as_view(), name='medical_knowledge_root'),
    path('topics/', MedicalKnowledgeListView.as_view(), name='knowledge_list'),
    path('topics/<slug:slug>/', MedicalKnowledgeDetailView.as_view(), name='knowledge_detail'),
    path('symptoms/dictionary/', SymptomDictionaryView.as_view(), name='symptom_dictionary'),
    path('symptoms/analyze/', SymptomAnalyzerView.as_view(), name='symptom_analyze'),
]

