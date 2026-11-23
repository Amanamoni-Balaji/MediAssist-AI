import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from nlp_engine.service import NLPService
from nlp_engine.preprocessor import TextPreprocessor
from nlp_engine.emergency import EmergencyDetector
from nlp_engine.intent_classifier import IntentClassifier
from nlp_engine.entity_extractor import MedicalEntityExtractor
from medical_knowledge.models import MedicalKnowledge
from conversations.models import Conversation, ChatMessage

class NLPProcessingTestCase(TestCase):
    def setUp(self):
        self.preprocessor = TextPreprocessor()
        self.emergency_detector = EmergencyDetector()
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = MedicalEntityExtractor()
        self.nlp_service = NLPService.get_instance()

    def test_preprocessor(self):
        sample = "What are the common symptoms of Diabetes in adults?"
        processed = self.preprocessor.preprocess(sample)
        self.assertIn("symptom", processed)
        self.assertIn("diabetes", processed)

    def test_emergency_detector(self):
        emergency_text = "I have crushing chest pain radiating to left arm and cannot breathe"
        is_em, msg = self.emergency_detector.check(emergency_text)
        self.assertTrue(is_em)
        self.assertIn("CRITICAL MEDICAL ADVISORY", msg)

        normal_text = "How much water should I drink every day?"
        is_em2, _ = self.emergency_detector.check(normal_text)
        self.assertFalse(is_em2)

    def test_intent_classification(self):
        sample = "What is hypertension?"
        intent, conf, _ = self.intent_classifier.predict(sample)
        self.assertIn(intent, ["disease_info", "general_faq"])
        self.assertGreater(conf, 0.2)

    def test_entity_extractor(self):
        sample = "I have had severe headache and high fever for 3 days"
        entities = self.entity_extractor.extract(sample)
        self.assertIn("headache", entities["symptoms"])
        self.assertIn("fever", entities["symptoms"])
        self.assertIn("severe", entities["severity"])

    def test_full_nlp_service_pipeline(self):
        res = self.nlp_service.process_message("What are common symptoms of fever?")
        self.assertFalse(res["is_emergency"])
        self.assertIn("response", res)
        self.assertTrue(len(res["response"]) > 20)
        self.assertIn("Medical Disclaimer", res["response"])


class APIScenarioTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testpatient',
            email='patient@test.com',
            password='Password123!',
            first_name='Test',
            last_name='User'
        )
        self.user.profile.medical_disclaimer_accepted = True
        self.user.profile.save()

        # Create sample medical knowledge
        self.mk = MedicalKnowledge.objects.create(
            topic="Type 2 Diabetes",
            slug="type-2-diabetes",
            category="Endocrine & Metabolic",
            description="Type 2 diabetes affects insulin metabolism.",
            symptoms=["excessive thirst", "frequent urination"],
            causes="Genetic and lifestyle factors",
            prevention="Healthy diet and regular exercise",
            when_to_seek_care="Seek urgent care if blood glucose spikes or ketoacidosis occurs",
            references=[{"source": "WHO", "title": "Diabetes", "url": "https://who.int"}],
            keywords="diabetes, blood sugar, insulin"
        )

    def test_user_login(self):
        res = self.client.post('/api/auth/login/', {
            'username': 'testpatient',
            'password': 'Password123!'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn('access', res.data)

    def test_medical_knowledge_endpoints(self):
        res = self.client.get('/api/medical/topics/')
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

        res_detail = self.client.get(f'/api/medical/topics/{self.mk.slug}/')
        self.assertEqual(res_detail.status_code, 200)
        self.assertEqual(res_detail.data['topic'], "Type 2 Diabetes")

    def test_chat_pipeline_endpoint(self):
        res = self.client.post('/api/chat/chat/send/', {
            'message': 'What is diabetes?'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn('assistant_message', res.data)
        self.assertIn('conversation_id', res.data)
        self.assertIn('nlp_metadata', res.data)

    def test_symptom_analyzer_endpoint(self):
        res = self.client.post('/api/medical/symptoms/analyze/', {
            'symptoms': ['excessive thirst', 'frequent urination']
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn('identified_conditions', res.data)
        self.assertFalse(res.data['is_emergency'])

    def test_feedback_submission(self):
        res = self.client.post('/api/feedback/submit/', {
            'is_helpful': True,
            'rating': 5,
            'comment': 'Accurate and safe response.'
        })
        self.assertEqual(res.status_code, 201)
        self.assertTrue(res.data['is_helpful'])
