#!/usr/bin/env python3
"""Test script to verify credentials.json is valid"""
import json
import os

def test_credentials():
    creds_path = 'credentials.json'
    
    print("[TEST] Checking credentials.json...")
    
    if not os.path.exists(creds_path):
        print(f"❌ File not found: {creds_path}")
        return False
    
    print(f"✅ File exists: {creds_path}")
    
    try:
        with open(creds_path, 'r') as f:
            creds_data = json.load(f)
        print("✅ Valid JSON format")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    
    # Check structure
    if 'web' not in creds_data:
        print("❌ Missing 'web' section")
        return False
    print("✅ Has 'web' section")
    
    web = creds_data['web']
    
    required = ['client_id', 'client_secret', 'auth_uri', 'token_uri', 'redirect_uris']
    for field in required:
        if field not in web:
            print(f"❌ Missing field: {field}")
            return False
        print(f"✅ Has {field}: {web[field] if field != 'client_secret' else '***'}")
    
    # Check if auth_uri is new format (not old deprecated format)
    if 'oauth2/auth' in web['auth_uri']:
        print("⚠️  WARNING: Using deprecated auth_uri format. Should be: https://accounts.google.com/o/oauth2/auth")
    
    # Check redirect_uris
    redirect = web['redirect_uris'][0]
    if 'localhost:8080' in redirect:
        print(f"✅ Redirect URI configured: {redirect}")
    else:
        print(f"❌ Unexpected redirect URI: {redirect}")
        print("   Expected: http://localhost:8080/oauth2callback")
        return False
    
    print("\n✅ All checks passed! Credentials look valid.")
    return True

if __name__ == '__main__':
    test_credentials()
