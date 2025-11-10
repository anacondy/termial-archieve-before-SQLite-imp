#!/usr/bin/env python3
"""
Comprehensive test suite for Terminal Archive application
Tests all features including routes, file upload, and UI components
"""

import os
import sys
import tempfile
import unittest
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestTerminalArchive(unittest.TestCase):
    """Test cases for Terminal Archive application"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
        self.client = self.app.test_client()
        
    def tearDown(self):
        """Clean up after each test"""
        # Clean up temporary upload directory
        import shutil
        if os.path.exists(self.app.config['UPLOAD_FOLDER']):
            shutil.rmtree(self.app.config['UPLOAD_FOLDER'])
    
    def test_index_route(self):
        """Test that index page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Terminal', response.data)
        print("✓ Index route test passed")
    
    def test_upload_page_route(self):
        """Test that upload page loads correctly"""
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload', response.data)
        print("✓ Upload page route test passed")
    
    def test_file_upload_pdf(self):
        """Test PDF file upload"""
        data = {
            'file': (BytesIO(b'PDF content'), 'test.pdf')
        }
        response = self.client.post('/upload', 
                                   data=data,
                                   content_type='multipart/form-data',
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("✓ PDF file upload test passed")
    
    def test_file_upload_txt(self):
        """Test TXT file upload"""
        data = {
            'file': (BytesIO(b'Text content'), 'test.txt')
        }
        response = self.client.post('/upload', 
                                   data=data,
                                   content_type='multipart/form-data',
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("✓ TXT file upload test passed")
    
    def test_invalid_file_type(self):
        """Test that invalid file types are rejected"""
        data = {
            'file': (BytesIO(b'Invalid content'), 'test.exe')
        }
        response = self.client.post('/upload', 
                                   data=data,
                                   content_type='multipart/form-data',
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid file type', response.data)
        print("✓ Invalid file type rejection test passed")
    
    def test_no_file_selected(self):
        """Test upload with no file selected"""
        data = {
            'file': (BytesIO(b''), '')
        }
        response = self.client.post('/upload', 
                                   data=data,
                                   content_type='multipart/form-data',
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("✓ No file selected test passed")
    
    def test_static_files_accessible(self):
        """Test that static files are accessible"""
        static_files = ['style.css', 'script.js', 'upload.js']
        for filename in static_files:
            response = self.client.get(f'/static/{filename}')
            self.assertEqual(response.status_code, 200)
            print(f"✓ Static file {filename} accessible")
    
    def test_404_handler(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        print("✓ 404 handler test passed")

class TestFileValidation(unittest.TestCase):
    """Test file validation functions"""
    
    def test_allowed_file_pdf(self):
        """Test PDF file is allowed"""
        from app import allowed_file
        self.assertTrue(allowed_file('test.pdf'))
        print("✓ PDF file validation passed")
    
    def test_allowed_file_doc(self):
        """Test DOC file is allowed"""
        from app import allowed_file
        self.assertTrue(allowed_file('test.doc'))
        print("✓ DOC file validation passed")
    
    def test_allowed_file_docx(self):
        """Test DOCX file is allowed"""
        from app import allowed_file
        self.assertTrue(allowed_file('test.docx'))
        print("✓ DOCX file validation passed")
    
    def test_allowed_file_txt(self):
        """Test TXT file is allowed"""
        from app import allowed_file
        self.assertTrue(allowed_file('test.txt'))
        print("✓ TXT file validation passed")
    
    def test_disallowed_file(self):
        """Test that invalid extensions are rejected"""
        from app import allowed_file
        self.assertFalse(allowed_file('test.exe'))
        self.assertFalse(allowed_file('test.jpg'))
        self.assertFalse(allowed_file('test.zip'))
        print("✓ Invalid file rejection test passed")

def run_tests():
    """Run all tests and display results"""
    print("=" * 70)
    print("Terminal Archive - Comprehensive Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestTerminalArchive))
    suite.addTests(loader.loadTestsFromTestCase(TestFileValidation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
