import sys
import os
import unittest

# Append the api directory to path so index can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
from index import app

class TestRisingWatersApp(unittest.TestCase):

    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.client = app.test_client()

    def test_home_page(self):
        """Test that the home page renders successfully and contains branding."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Rising Waters', response.data)
        self.assertIn(b'Intelligent Flood Risk Forecasting', response.data)

    def test_predictor_page(self):
        """Test that the prediction form renders successfully and contains fields."""
        response = self.client.get('/Predict')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Meteorological Prediction Form', response.data)
        self.assertIn(b'Cloud Cover', response.data)

    def test_predict_low_risk(self):
        """Test that low-risk parameters redirect to /no_chance."""
        low_risk_data = {
            "cloud": "5.0",
            "annual": "1200.0",
            "janfeb": "5.0",
            "marMay": "20.0",
            "juneSept": "700.0"
        }
        response = self.client.post('/predict', data=low_risk_data)
        # Expect redirect (302)
        self.assertEqual(response.status_code, 302)
        # Location header should redirect to /no_chance with parameters
        self.assertIn('/no_chance', response.headers['Location'])
        self.assertIn('prob=', response.headers['Location'])

    def test_predict_high_risk(self):
        """Test that high-risk parameters redirect to /chance."""
        high_risk_data = {
            "cloud": "90.0",
            "annual": "4500.0",
            "janfeb": "95.0",
            "marMay": "650.0",
            "juneSept": "3200.0"
        }
        response = self.client.post('/predict', data=high_risk_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/chance', response.headers['Location'])
        self.assertIn('prob=', response.headers['Location'])

    def test_validation_negative_input(self):
        """Test that negative rainfall parameters fail validation and redirect to form."""
        invalid_data = {
            "cloud": "50.0",
            "annual": "-1000.0",
            "janfeb": "10.0",
            "marMay": "15.0",
            "juneSept": "20.0"
        }
        response = self.client.post('/predict', data=invalid_data)
        self.assertEqual(response.status_code, 302)
        # Should redirect back to prediction form page
        self.assertIn('/index', response.headers['Location'])

        # Verify flash message gets set in the session
        with self.client.session_transaction() as session:
            flashes = session.get('_flashes', [])
            self.assertTrue(any("cannot be negative" in f[1] for f in flashes))

    def test_validation_range_cloud_cover(self):
        """Test that cloud cover > 100% fails validation."""
        invalid_data = {
            "cloud": "105.0",
            "annual": "2000.0",
            "janfeb": "10.0",
            "marMay": "15.0",
            "juneSept": "20.0"
        }
        response = self.client.post('/predict', data=invalid_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/index', response.headers['Location'])
        
        with self.client.session_transaction() as session:
            flashes = session.get('_flashes', [])
            self.assertTrue(any("Cloud Cover must be between" in f[1] for f in flashes))

    def test_validation_logical_check(self):
        """Test that seasonal sum exceeding annual rainfall fails validation."""
        invalid_data = {
            "cloud": "50.0",
            "annual": "1000.0",
            "janfeb": "500.0",
            "marMay": "400.0",
            "juneSept": "300.0" # sum = 1200 > 1000
        }
        response = self.client.post('/predict', data=invalid_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/index', response.headers['Location'])
        
        with self.client.session_transaction() as session:
            flashes = session.get('_flashes', [])
            self.assertTrue(any("cannot exceed the total Annual Rainfall" in f[1] for f in flashes))

    def test_chance_renders(self):
        """Test that the /chance route renders properly with query parameters."""
        response = self.client.get('/chance?prob=98.55&cloud=80&annual=3500&janfeb=50&marmay=400&junesep=2500')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'High Flood Risk Detected!', response.data)
        self.assertIn(b'98.55%', response.data)
        self.assertIn(b'3500 mm', response.data)

    def test_no_chance_renders(self):
        """Test that the /no_chance route renders properly with query parameters."""
        response = self.client.get('/no_chance?prob=92.10&cloud=15&annual=1000&janfeb=10&marmay=80&junesep=600')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Low Flood Risk Detected', response.data)
        self.assertIn(b'92.10%', response.data)
        self.assertIn(b'1000 mm', response.data)

if __name__ == '__main__':
    unittest.main()
