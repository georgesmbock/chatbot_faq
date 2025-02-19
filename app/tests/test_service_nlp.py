#!/usr/venvs/transformers/bin/python3
"""Service NLP test"""
import unittest
import os
from services.nlp_service import loadJsonFile, predict_question

class TestNLPService(unittest.TestCase):
    """Class of tests for the NLP Service"""

    def setUp(self):
        # Vérifiez si les fichiers nécessaires existent
        self.dataset_path = '../data/dataset/faq_dataset.json'
        self.model_path = '../data/file_nlp'
        if not os.path.exists(self.dataset_path):
            self.fail(f"Dataset file not found: {self.dataset_path}")
        if not os.path.exists(self.model_path):
            self.fail(f"Model files not found: {self.model_path}")
        
        # Charger les données pour les tests
        self.data = loadJsonFile()
        self.user_question = "How do I return an item?"
        self.response_bot = {
            "answer": "Yes, returns are accepted within 30 days with a valid receipt.",
            "question": "How do I return an item?",
            "idQuestion": "proq13"
        }

    def tearDown(self):
        pass

    def test_NLPService(self):
        # Tester la fonction predict_question
        question_id, answer, _ = predict_question(self.user_question)
        self.assertEqual(question_id, self.response_bot["idQuestion"])
        self.assertEqual(answer, self.response_bot["answer"])


if __name__ == '__main__':
    unittest.main()
