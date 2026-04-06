#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for OpenClaw Clone AI Personal Assistant
Tests all endpoints specified in the review request.
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class OpenClawAPITester:
    def __init__(self, base_url: str = "https://buddy-automation.preview.emergentagent.com"):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.refresh_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
        # Test credentials from agent context
        self.test_email = "test@example.com"
        self.test_password = "Password@12345!"

    def log_test(self, name: str, success: bool, details: Dict[str, Any] = None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
        
        result = {
            "test_name": name,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details or {}
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details and not success:
            print(f"   Details: {details}")

    def make_request(self, method: str, endpoint: str, data: Dict = None, 
                    headers: Dict = None, expected_status: int = 200) -> tuple[bool, Dict]:
        """Make HTTP request and validate response"""
        url = f"{self.base_url}{endpoint}"
        request_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            request_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            request_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=request_headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=request_headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=request_headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=request_headers, timeout=30)
            else:
                return False, {"error": f"Unsupported method: {method}"}

            success = response.status_code == expected_status
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text, "status_code": response.status_code}

            return success, response_data

        except requests.exceptions.RequestException as e:
            return False, {"error": str(e), "endpoint": endpoint}

    def test_health_endpoint(self):
        """Test /api/health endpoint"""
        success, response = self.make_request('GET', '/api/health')
        
        if success and response.get('success') and response.get('status') == 'ok':
            self.log_test("Health Endpoint", True, {"response": response})
        else:
            self.log_test("Health Endpoint", False, {"response": response})

    def test_user_login(self):
        """Test user login with provided credentials"""
        login_data = {
            "email": self.test_email,
            "password": self.test_password
        }
        
        success, response = self.make_request('POST', '/api/auth/login', data=login_data)
        
        if success and response.get('success') and response.get('token'):
            self.token = response.get('token')
            self.refresh_token = response.get('refresh_token')
            self.log_test("User Login", True, {
                "email": self.test_email,
                "email_verified": response.get('email_verified'),
                "user": response.get('user')
            })
            return True
        else:
            self.log_test("User Login", False, {"response": response})
            return False

    def test_user_registration(self):
        """Test user registration with new credentials"""
        # Generate unique email for registration test
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reg_email = f"test_reg_{timestamp}@example.com"
        
        reg_data = {
            "email": reg_email,
            "password": "TestPassword123!",
            "name": "Test User Registration"
        }
        
        success, response = self.make_request('POST', '/api/auth/register', data=reg_data, expected_status=201)
        
        if success and response.get('success') and response.get('token'):
            self.log_test("User Registration", True, {
                "email": reg_email,
                "user": response.get('user'),
                "verification_code_provided": bool(response.get('verification_code_dev_only'))
            })
        else:
            self.log_test("User Registration", False, {"response": response})

    def test_get_user_profile(self):
        """Test /api/auth/me endpoint"""
        if not self.token:
            self.log_test("Get User Profile", False, {"error": "No auth token available"})
            return
            
        success, response = self.make_request('GET', '/api/auth/me')
        
        if success and response.get('success') and response.get('user'):
            user = response.get('user')
            self.log_test("Get User Profile", True, {
                "user_id": user.get('id'),
                "email": user.get('email'),
                "email_verified": user.get('email_verified')
            })
        else:
            self.log_test("Get User Profile", False, {"response": response})

    def test_token_refresh(self):
        """Test /api/auth/refresh endpoint"""
        if not self.refresh_token:
            self.log_test("Token Refresh", False, {"error": "No refresh token available"})
            return
            
        refresh_data = {"refresh_token": self.refresh_token}
        success, response = self.make_request('POST', '/api/auth/refresh', data=refresh_data)
        
        if success and response.get('success') and response.get('token'):
            # Update tokens
            self.token = response.get('token')
            self.refresh_token = response.get('refresh_token')
            self.log_test("Token Refresh", True, {"new_token_received": True})
        else:
            self.log_test("Token Refresh", False, {"response": response})

    def test_process_command(self):
        """Test /api/command endpoint"""
        if not self.token:
            self.log_test("Process Command", False, {"error": "No auth token available"})
            return
            
        command_data = {
            "command": "What's the weather like today?",
            "type": "text",
            "context": {"conversation_id": "test_conv_001"}
        }
        
        success, response = self.make_request('POST', '/api/command', data=command_data)
        
        if success and response.get('success'):
            self.log_test("Process Command", True, {
                "conversation_id": response.get('conversation_id'),
                "response_text": response.get('response', {}).get('text'),
                "action_taken": response.get('response', {}).get('action_taken')
            })
        else:
            self.log_test("Process Command", False, {"response": response})

    def test_get_skills(self):
        """Test /api/skills endpoint"""
        if not self.token:
            self.log_test("Get Skills List", False, {"error": "No auth token available"})
            return
            
        success, response = self.make_request('GET', '/api/skills')
        
        if success and response.get('success'):
            skills = response.get('skills', [])
            self.log_test("Get Skills List", True, {
                "skills_count": len(skills),
                "skill_names": [s.get('name') for s in skills[:5]]  # First 5 skills
            })
        else:
            self.log_test("Get Skills List", False, {"response": response})

    def test_get_schedules(self):
        """Test /api/schedules endpoint"""
        if not self.token:
            self.log_test("Get Schedules List", False, {"error": "No auth token available"})
            return
            
        success, response = self.make_request('GET', '/api/schedules')
        
        if success and response.get('success'):
            schedules = response.get('schedules', [])
            self.log_test("Get Schedules List", True, {
                "schedules_count": len(schedules)
            })
        else:
            self.log_test("Get Schedules List", False, {"response": response})

    def test_get_integrations(self):
        """Test /api/integrations endpoint"""
        if not self.token:
            self.log_test("Get Integrations Status", False, {"error": "No auth token available"})
            return
            
        success, response = self.make_request('GET', '/api/integrations')
        
        if success and response.get('success'):
            integrations = response.get('integrations', [])
            connected_count = sum(1 for i in integrations if i.get('status') == 'connected')
            self.log_test("Get Integrations Status", True, {
                "total_integrations": len(integrations),
                "connected_integrations": connected_count,
                "integration_names": [i.get('name') for i in integrations]
            })
        else:
            self.log_test("Get Integrations Status", False, {"response": response})

    def test_desktop_status(self):
        """Test /api/desktop/status endpoint"""
        if not self.token:
            self.log_test("Desktop Status", False, {"error": "No auth token available"})
            return
            
        success, response = self.make_request('GET', '/api/desktop/status')
        
        if success and response.get('success'):
            status = response.get('status')
            agent_info = response.get('agent_info')
            self.log_test("Desktop Status", True, {
                "status": status,
                "agent_connected": status == 'connected',
                "agent_info": agent_info
            })
        else:
            self.log_test("Desktop Status", False, {"response": response})

    def run_all_tests(self):
        """Run all API tests in sequence"""
        print("🚀 Starting OpenClaw Clone API Testing...")
        print(f"📍 Base URL: {self.base_url}")
        print(f"👤 Test User: {self.test_email}")
        print("=" * 60)
        
        # Test health endpoint first (no auth required)
        self.test_health_endpoint()
        
        # Test authentication flow
        login_success = self.test_user_login()
        
        # Test registration (independent of login)
        self.test_user_registration()
        
        if login_success:
            # Test authenticated endpoints
            self.test_get_user_profile()
            self.test_token_refresh()
            self.test_process_command()
            self.test_get_skills()
            self.test_get_schedules()
            self.test_get_integrations()
            self.test_desktop_status()
        else:
            print("⚠️  Skipping authenticated endpoint tests due to login failure")
        
        # Print summary
        print("=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print("❌ Some tests failed. Check details above.")
            return 1

def main():
    """Main test execution"""
    tester = OpenClawAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())