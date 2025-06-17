#!/usr/bin/env python3
"""
Test script to verify basic dependencies work
"""
import sys

def test_imports():
    """Test if all required imports work"""
    try:
        import flask
        print(f"✅ Flask imported successfully: {flask.__version__}")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import requests
        print(f"✅ Requests imported successfully: {requests.__version__}")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        import yaml
        print(f"✅ PyYAML imported successfully: {yaml.__version__}")
    except ImportError as e:
        print(f"❌ PyYAML import failed: {e}")
        return False
    
    try:
        import urllib3
        print(f"✅ urllib3 imported successfully: {urllib3.__version__}")
    except ImportError as e:
        print(f"❌ urllib3 import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality"""
    try:
        from flask import Flask
        app = Flask(__name__)
        print("✅ Flask app creation successful")
        
        import requests
        response = requests.get("https://httpbin.org/get", timeout=5)
        print(f"✅ HTTP request successful: {response.status_code}")
        
        import yaml
        data = {"test": "value"}
        yaml_str = yaml.dump(data)
        print(f"✅ YAML serialization successful: {yaml_str.strip()}")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing dependencies...")
    print("=" * 50)
    
    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()
    
    print("=" * 50)
    if imports_ok and functionality_ok:
        print("✅ All tests passed! Dependencies are working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the errors above.")
        sys.exit(1) 