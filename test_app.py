#!/usr/bin/env python3
"""
Basic test suite for Terminal Archives application
Run with: python test_app.py
"""

import sys
from app import app, sanitize, allowed_file

def test_sanitize():
    """Test input sanitization function"""
    print("Testing sanitize function...")
    
    # Test normal text
    assert sanitize('normal text') == 'normal text', "Normal text failed"
    
    # Test path traversal attempts
    assert sanitize('path/../traversal') == 'pathtraversal', "Path traversal prevention failed"
    assert sanitize('../../etc/passwd') == 'etcpasswd', "Path traversal prevention failed"
    
    # Test XSS attempts
    assert sanitize('test<script>alert(1)</script>') == 'testscriptalert1script', "XSS prevention failed"
    assert sanitize('"><script>alert(1)</script>') == 'scriptalert1script', "XSS prevention failed"
    
    # Test length limiting
    assert sanitize('a' * 150) == 'a' * 100, "Length limit failed"
    
    # Test special characters
    assert '/' not in sanitize('test/path'), "Slash not removed"
    assert '\\' not in sanitize('test\\path'), "Backslash not removed"
    
    # Test empty input
    assert sanitize('') == '', "Empty string failed"
    assert sanitize(None) == '', "None handling failed"
    
    print("✓ Sanitize tests passed")

def test_allowed_file():
    """Test file validation function"""
    print("Testing allowed_file function...")
    
    # Test valid PDF files
    assert allowed_file('test.pdf') == True, "Valid PDF failed"
    assert allowed_file('test.PDF') == True, "Case-insensitive PDF failed"
    assert allowed_file('my-paper.pdf') == True, "PDF with hyphen failed"
    
    # Test invalid files
    assert allowed_file('test.exe') == False, "EXE should be rejected"
    assert allowed_file('test.txt') == False, "TXT should be rejected"
    assert allowed_file('test.doc') == False, "DOC should be rejected"
    assert allowed_file('no_extension') == False, "No extension should be rejected"
    assert allowed_file('') == False, "Empty string should be rejected"
    
    # Test edge cases
    assert allowed_file('file.pdf.exe') == False, "Double extension should be rejected"
    
    print("✓ File validation tests passed")

def test_flask_config():
    """Test Flask application configuration"""
    print("Testing Flask configuration...")
    
    # Test max content length (50 MB)
    assert app.config['MAX_CONTENT_LENGTH'] == 50 * 1024 * 1024, "Max content length misconfigured"
    
    # Test secret key exists
    assert app.config['SECRET_KEY'] is not None, "Secret key not set"
    assert len(app.config['SECRET_KEY']) > 0, "Secret key is empty"
    
    # Test upload folder
    assert app.config['UPLOAD_FOLDER'] == 'uploads', "Upload folder misconfigured"
    
    print("✓ Configuration tests passed")

def test_routes():
    """Test Flask routes are registered"""
    print("Testing route registration...")
    
    routes = [str(rule) for rule in app.url_map.iter_rules()]
    
    # Test required routes exist
    required_routes = ['/', '/admin', '/upload', '/api/papers', '/uploads/<path:filename>']
    for route in required_routes:
        assert any(route in r for r in routes), f"Route {route} not found"
    
    print("✓ Route registration tests passed")

def test_security_headers():
    """Test security headers are properly configured"""
    print("Testing security headers...")
    
    with app.test_client() as client:
        response = client.get('/')
        
        # Check for security headers
        assert 'X-Frame-Options' in response.headers, "X-Frame-Options missing"
        assert 'X-Content-Type-Options' in response.headers, "X-Content-Type-Options missing"
        assert 'X-XSS-Protection' in response.headers, "X-XSS-Protection missing"
        assert 'Content-Security-Policy' in response.headers, "CSP missing"
        assert 'Referrer-Policy' in response.headers, "Referrer-Policy missing"
        
        # Check header values
        assert response.headers['X-Frame-Options'] == 'SAMEORIGIN', "X-Frame-Options incorrect"
        assert response.headers['X-Content-Type-Options'] == 'nosniff', "X-Content-Type-Options incorrect"
        
    print("✓ Security headers tests passed")

def test_api_endpoint():
    """Test API endpoint returns proper JSON"""
    print("Testing API endpoint...")
    
    with app.test_client() as client:
        response = client.get('/api/papers')
        
        # Check response is JSON
        assert response.content_type == 'application/json', "Response not JSON"
        
        # Check response is valid JSON (list)
        data = response.get_json()
        assert isinstance(data, list), "Response should be a list"
        
    print("✓ API endpoint tests passed")

def test_404_handling():
    """Test 404 error handling"""
    print("Testing 404 handling...")
    
    with app.test_client() as client:
        response = client.get('/nonexistent-page')
        assert response.status_code == 404, "404 not returned for nonexistent page"
        
    print("✓ 404 handling tests passed")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Terminal Archives Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_sanitize()
        test_allowed_file()
        test_flask_config()
        test_routes()
        test_security_headers()
        test_api_endpoint()
        test_404_handling()
        
        print()
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ ERROR: {e}")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
