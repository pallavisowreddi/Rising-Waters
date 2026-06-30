import sys
import os
import unittest
import json

# Import app from the main entrypoint
from main import app

class TestRisingWatersApp(unittest.TestCase):

    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.client = app.test_client()

    def test_home_page(self):
        """Test that the home page (dashboard) renders successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Intelligent Flood Risk Forecasting', response.data)
        self.assertIn(b'Model Performance', response.data)

    def test_predictor_page(self):
        """Test that the predictor form page renders successfully."""
        response = self.client.get('/predictor')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flood Risk Predictor Form', response.data)
        self.assertIn(b'Cloud Cover', response.data)

    def test_docs_page(self):
        """Test that the technical specs page renders successfully."""
        response = self.client.get('/docs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Model Specifications', response.data)
        self.assertIn(b'Confusion Matrix', response.data)

    def test_portal_page(self):
        """Test that the project docs portal page renders successfully."""
        response = self.client.get('/portal')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project Documentations Portal', response.data)
        self.assertIn(b'marked.min.js', response.data)

    def test_predict_low_risk(self):
        """Test that low-risk parameters return Low Flood Risk JSON."""
        low_risk_data = {
            "ID": "TST-LOW",
            "cloud": 15.0,
            "annual": 1200.0,
            "janfeb": 10.0,
            "marMay": 80.0,
            "juneSept": 700.0
        }
        response = self.client.post('/predict', json=low_risk_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["prediction"], "Low Flood Risk")
        self.assertEqual(data["applicant_id"], "TST-LOW")
        self.assertTrue("probability" in data)
        self.assertTrue("reason" in data)

    def test_predict_high_risk(self):
        """Test that high-risk parameters return High Flood Risk JSON."""
        high_risk_data = {
            "ID": "TST-HIGH",
            "cloud": 90.0,
            "annual": 4500.0,
            "janfeb": 90.0,
            "marMay": 600.0,
            "juneSept": 3200.0
        }
        response = self.client.post('/predict', json=high_risk_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["prediction"], "High Flood Risk")
        self.assertEqual(data["applicant_id"], "TST-HIGH")

    def test_validation_negative_input(self):
        """Test that negative rainfall parameters fail validation."""
        invalid_data = {
            "ID": "TST-NEG",
            "cloud": 50.0,
            "annual": -1000.0,
            "janfeb": 10.0,
            "marMay": 15.0,
            "juneSept": 20.0
        }
        response = self.client.post('/predict', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue("error" in data)
        self.assertIn("cannot be negative", data["error"])

    def test_validation_range_cloud_cover(self):
        """Test that cloud cover > 100% fails validation."""
        invalid_data = {
            "ID": "TST-RANGE",
            "cloud": 105.0,
            "annual": 2000.0,
            "janfeb": 10.0,
            "marMay": 15.0,
            "juneSept": 20.0
        }
        response = self.client.post('/predict', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn("Cloud Cover must be between", data["error"])

    def test_validation_logical_check(self):
        """Test that seasonal sum exceeding annual rainfall fails validation."""
        invalid_data = {
            "ID": "TST-LOGIC",
            "cloud": 50.0,
            "annual": 1000.0,
            "janfeb": 500.0,
            "marMay": 400.0,
            "juneSept": 300.0 # sum = 1200 > 1000
        }
        response = self.client.post('/predict', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn("cannot exceed the total Annual Rainfall", data["error"])

    def test_api_docs_list(self):
        """Test the dynamic documentation list endpoint."""
        response = self.client.get('/api/project-docs/list')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue("folders" in data)
        # Check if first folder exists in catalog
        if len(data["folders"]) > 0:
            self.assertTrue("name" in data["folders"][0])
            self.assertTrue("files" in data["folders"][0])

if __name__ == '__main__':
    unittest.main()
