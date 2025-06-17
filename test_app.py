#!/usr/bin/env python3
"""
Unit tests for the Security Test Application
"""
import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
from app import app

class TestSecurityApp(unittest.TestCase):
    """Test cases for the Security Test Application"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Set environment variables for testing
        os.environ['SAST_VULNS'] = 'false'
        os.environ['SCM_VULNS'] = 'false'
        os.environ['DAST_VULNS'] = 'false'
        os.environ['XSS_VULN'] = 'false'
        os.environ['SQL_INJECTION_VULN'] = 'false'
        os.environ['COMMAND_INJECTION_VULN'] = 'false'
        os.environ['PATH_TRAVERSAL_VULN'] = 'false'
        os.environ['HARDCODED_SECRETS_VULN'] = 'false'
        os.environ['INSECURE_DEPENDENCIES'] = 'false'

    def test_home_page(self):
        """Test home page loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Security Test Application', response.data)

    def test_echo_endpoint(self):
        """Test echo endpoint"""
        test_data = {"test": "value"}
        response = self.app.post('/api/echo', 
                               data=json.dumps(test_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['echo'], test_data)

    def test_config_endpoint(self):
        """Test config endpoint returns correct values"""
        response = self.app.get('/api/config')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check that all vulnerabilities are disabled
        self.assertFalse(data['sast_vulns'])
        self.assertFalse(data['scm_vulns'])
        self.assertFalse(data['dast_vulns'])
        self.assertFalse(data['xss_vuln'])
        self.assertFalse(data['sql_injection_vuln'])
        self.assertFalse(data['command_injection_vuln'])
        self.assertFalse(data['path_traversal_vuln'])
        self.assertFalse(data['hardcoded_secrets_vuln'])
        self.assertFalse(data['insecure_dependencies_vuln'])

    def test_health_endpoint(self):
        """Test health endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('vulnerabilities', data)

    def test_user_endpoint_disabled(self):
        """Test user endpoint when SQL injection is disabled"""
        response = self.app.get('/api/user/123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('disabled', data['message'])

    def test_ping_endpoint_disabled(self):
        """Test ping endpoint when command injection is disabled"""
        test_data = {"host": "localhost"}
        response = self.app.post('/api/ping',
                               data=json.dumps(test_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('disabled', data['message'])

    def test_secrets_endpoint_disabled(self):
        """Test secrets endpoint when hardcoded secrets are disabled"""
        response = self.app.get('/api/secrets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('disabled', data['message'])

    def test_dependencies_endpoint_disabled(self):
        """Test dependencies endpoint when insecure dependencies are disabled"""
        response = self.app.get('/api/dependencies')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('disabled', data['message'])

    def test_file_endpoint_disabled(self):
        """Test file endpoint when path traversal is disabled"""
        response = self.app.get('/api/file/test.txt')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('disabled', data['message'])

    def test_headers_endpoint_disabled(self):
        """Test headers endpoint when DAST vulnerabilities are disabled"""
        response = self.app.get('/api/headers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('disabled', data['message'])

    @patch.dict(os.environ, {'SAST_VULNS': 'true', 'SQL_INJECTION_VULN': 'true'})
    def test_user_endpoint_enabled(self):
        """Test user endpoint when SQL injection is enabled"""
        response = self.app.get('/api/user/123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('users', data)

    @patch.dict(os.environ, {'SAST_VULNS': 'true', 'COMMAND_INJECTION_VULN': 'true'})
    def test_ping_endpoint_enabled(self):
        """Test ping endpoint when command injection is enabled"""
        test_data = {"host": "localhost"}
        response = self.app.post('/api/ping',
                               data=json.dumps(test_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('result', data)

    @patch.dict(os.environ, {'SCM_VULNS': 'true', 'HARDCODED_SECRETS_VULN': 'true'})
    def test_secrets_endpoint_enabled(self):
        """Test secrets endpoint when hardcoded secrets are enabled"""
        response = self.app.get('/api/secrets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('database_password', data)

    @patch.dict(os.environ, {'SCM_VULNS': 'true', 'INSECURE_DEPENDENCIES': 'true'})
    def test_dependencies_endpoint_enabled(self):
        """Test dependencies endpoint when insecure dependencies are enabled"""
        response = self.app.get('/api/dependencies')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('requests', data)

    @patch.dict(os.environ, {'DAST_VULNS': 'true', 'PATH_TRAVERSAL_VULN': 'true'})
    def test_file_endpoint_enabled(self):
        """Test file endpoint when path traversal is enabled"""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('test content')
            temp_file = f.name
        
        try:
            response = self.app.get(f'/api/file/{temp_file}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('content', data)
        finally:
            os.unlink(temp_file)

    @patch.dict(os.environ, {'DAST_VULNS': 'true'})
    def test_headers_endpoint_enabled(self):
        """Test headers endpoint when DAST vulnerabilities are enabled"""
        response = self.app.get('/api/headers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_invalid_json(self):
        """Test handling of invalid JSON"""
        response = self.app.post('/api/echo',
                               data='invalid json',
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_missing_content_type(self):
        """Test handling of missing content type"""
        response = self.app.post('/api/echo',
                               data='{"test": "value"}')
        self.assertEqual(response.status_code, 400)

    def test_404_endpoint(self):
        """Test 404 handling"""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_method_not_allowed(self):
        """Test method not allowed"""
        response = self.app.post('/health')
        self.assertEqual(response.status_code, 405)

    def test_environment_variables_parsing(self):
        """Test environment variable parsing"""
        # Test with various boolean values
        test_cases = [
            ('true', True),
            ('True', True),
            ('TRUE', True),
            ('false', False),
            ('False', False),
            ('FALSE', False),
            ('', False),
            ('invalid', False)
        ]
        
        for value, expected in test_cases:
            with patch.dict(os.environ, {'SAST_VULNS': value}):
                # Reimport app to get fresh environment variable parsing
                import importlib
                import app
                importlib.reload(app)
                
                # Check if the variable is parsed correctly
                self.assertEqual(app.SAST_VULNS, expected)

if __name__ == '__main__':
    unittest.main() 