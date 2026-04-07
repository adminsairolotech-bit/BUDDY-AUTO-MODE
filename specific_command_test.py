#!/usr/bin/env python3
"""
Test specific AI commands mentioned in the review request:
- Calculator command: 'Calculate 25 * 4' returns 100
- Translation command: 'Translate hello to Hindi' returns Hindi text
"""

import requests
import sys
import json
from datetime import datetime

class SpecificCommandTester:
    def __init__(self, base_url: str = "https://buddy-automation.preview.emergentagent.com"):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.test_email = "test@example.com"
        self.test_password = "Password@12345!"
        self.tests_run = 0
        self.tests_passed = 0

    def login(self):
        """Login to get auth token"""
        login_data = {
            "email": self.test_email,
            "password": self.test_password
        }
        
        response = requests.post(f"{self.base_url}/api/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('token'):
                self.token = data.get('token')
                print("✅ Login successful")
                return True
        
        print("❌ Login failed")
        return False

    def test_command(self, command: str, expected_keyword: str = None):
        """Test a specific command"""
        if not self.token:
            print("❌ No auth token available")
            return False

        command_data = {
            "command": command,
            "type": "text",
            "context": {"conversation_id": f"test_conv_{datetime.now().strftime('%H%M%S')}"}
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        
        self.tests_run += 1
        print(f"\n🔍 Testing command: '{command}'")
        
        try:
            response = requests.post(f"{self.base_url}/api/command", json=command_data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    response_text = data.get('response', {}).get('text', '')
                    print(f"✅ Command executed successfully")
                    print(f"📝 Response: {response_text}")
                    
                    # Check if expected keyword is in response
                    if expected_keyword and expected_keyword.lower() in response_text.lower():
                        print(f"✅ Expected result '{expected_keyword}' found in response")
                        self.tests_passed += 1
                        return True
                    elif not expected_keyword:
                        self.tests_passed += 1
                        return True
                    else:
                        print(f"❌ Expected result '{expected_keyword}' not found in response")
                        return False
                else:
                    print(f"❌ Command failed: {data}")
                    return False
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

    def run_specific_tests(self):
        """Run the specific tests mentioned in review request"""
        print("🚀 Testing Specific AI Commands...")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 60)
        
        # Login first
        if not self.login():
            return 1
        
        # Test calculator command
        print("\n📊 Testing Calculator Command...")
        calc_success = self.test_command("Calculate 25 * 4", "100")
        
        # Test translation command  
        print("\n🌐 Testing Translation Command...")
        trans_success = self.test_command("Translate hello to Hindi", "नमस्ते")
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All specific command tests passed!")
            return 0
        else:
            print("❌ Some command tests failed.")
            return 1

def main():
    """Main test execution"""
    tester = SpecificCommandTester()
    return tester.run_specific_tests()

if __name__ == "__main__":
    sys.exit(main())