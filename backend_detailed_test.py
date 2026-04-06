#!/usr/bin/env python3
"""
Detailed Backend API Testing with Response Validation
Tests the actual functionality and data integrity of each endpoint.
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class DetailedAPITester:
    def __init__(self, base_url: str = "https://buddy-automation.preview.emergentagent.com"):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.refresh_token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.detailed_results = []
        
        # Test credentials
        self.test_email = "test@example.com"
        self.test_password = "Password@12345!"

    def log_detailed_test(self, name: str, success: bool, response_data: Dict = None, validation_details: Dict = None):
        """Log detailed test result with response validation"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
        
        result = {
            "test_name": name,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
            "response_data": response_data or {},
            "validation_details": validation_details or {}
        }
        self.detailed_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if validation_details:
            for key, value in validation_details.items():
                print(f"   {key}: {value}")

    def make_request(self, method: str, endpoint: str, data: Dict = None, 
                    headers: Dict = None, expected_status: int = 200) -> tuple[bool, Dict]:
        """Make HTTP request and return response"""
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

    def test_health_detailed(self):
        """Detailed test of health endpoint"""
        success, response = self.make_request('GET', '/api/health')
        
        validation = {}
        if success:
            validation["has_success_field"] = "success" in response
            validation["success_value"] = response.get("success")
            validation["has_status_field"] = "status" in response
            validation["status_value"] = response.get("status")
            
            # Validate expected structure
            is_valid = (response.get("success") is True and 
                       response.get("status") == "ok")
            
            self.log_detailed_test("Health Endpoint Detailed", is_valid, response, validation)
        else:
            self.log_detailed_test("Health Endpoint Detailed", False, response, {"error": "Request failed"})

    def test_login_detailed(self):
        """Detailed test of login endpoint"""
        login_data = {
            "email": self.test_email,
            "password": self.test_password
        }
        
        success, response = self.make_request('POST', '/api/auth/login', data=login_data)
        
        validation = {}
        if success:
            validation["has_success_field"] = "success" in response
            validation["has_token"] = "token" in response
            validation["has_refresh_token"] = "refresh_token" in response
            validation["has_user_data"] = "user" in response
            validation["email_verified_field"] = "email_verified" in response
            
            user_data = response.get("user", {})
            validation["user_has_id"] = "id" in user_data
            validation["user_has_email"] = "email" in user_data
            validation["user_has_name"] = "name" in user_data
            validation["email_matches"] = user_data.get("email") == self.test_email
            
            # Store tokens and user ID for subsequent tests
            if response.get("token"):
                self.token = response.get("token")
                self.refresh_token = response.get("refresh_token")
                self.user_id = user_data.get("id")
            
            is_valid = (response.get("success") is True and 
                       response.get("token") and 
                       response.get("user", {}).get("email") == self.test_email)
            
            self.log_detailed_test("Login Detailed", is_valid, response, validation)
            return is_valid
        else:
            self.log_detailed_test("Login Detailed", False, response, {"error": "Login request failed"})
            return False

    def test_user_profile_detailed(self):
        """Detailed test of user profile endpoint"""
        if not self.token:
            self.log_detailed_test("User Profile Detailed", False, {}, {"error": "No auth token"})
            return
            
        success, response = self.make_request('GET', '/api/auth/me')
        
        validation = {}
        if success:
            validation["has_success_field"] = "success" in response
            validation["has_user_field"] = "user" in response
            
            user_data = response.get("user", {})
            validation["user_has_id"] = "id" in user_data
            validation["user_has_email"] = "email" in user_data
            validation["user_has_name"] = "name" in user_data
            validation["user_has_email_verified"] = "email_verified" in user_data
            validation["user_has_preferences"] = "preferences" in user_data
            validation["email_matches"] = user_data.get("email") == self.test_email
            validation["id_matches"] = user_data.get("id") == self.user_id
            
            is_valid = (response.get("success") is True and 
                       user_data.get("email") == self.test_email and
                       user_data.get("id") == self.user_id)
            
            self.log_detailed_test("User Profile Detailed", is_valid, response, validation)
        else:
            self.log_detailed_test("User Profile Detailed", False, response, {"error": "Profile request failed"})

    def test_command_processing_detailed(self):
        """Detailed test of command processing"""
        if not self.token:
            self.log_detailed_test("Command Processing Detailed", False, {}, {"error": "No auth token"})
            return
            
        # Test simple weather command
        command_data = {
            "command": "What's the weather like?",
            "type": "text",
            "context": {"conversation_id": "test_detailed_conv"}
        }
        
        success, response = self.make_request('POST', '/api/command', data=command_data)
        
        validation = {}
        if success:
            validation["has_success_field"] = "success" in response
            validation["has_response_field"] = "response" in response
            validation["has_conversation_id"] = "conversation_id" in response
            
            response_data = response.get("response", {})
            validation["response_has_text"] = "text" in response_data
            validation["response_has_action_taken"] = "action_taken" in response_data
            
            action_taken = response_data.get("action_taken", {})
            validation["action_has_type"] = "type" in action_taken
            validation["action_has_status"] = "status" in action_taken
            validation["action_has_details"] = "details" in action_taken
            
            validation["conversation_id_value"] = response.get("conversation_id")
            validation["response_text_length"] = len(response_data.get("text", ""))
            
            is_valid = (response.get("success") is True and 
                       response_data.get("text") and
                       action_taken.get("type") and
                       response.get("conversation_id"))
            
            self.log_detailed_test("Command Processing Detailed", is_valid, response, validation)
        else:
            self.log_detailed_test("Command Processing Detailed", False, response, {"error": "Command request failed"})

    def test_skills_detailed(self):
        """Detailed test of skills endpoint"""
        if not self.token:
            self.log_detailed_test("Skills List Detailed", False, {}, {"error": "No auth token"})
            return
            
        success, response = self.make_request('GET', '/api/skills')
        
        validation = {}
        if success:
            validation["has_success_field"] = "success" in response
            validation["has_skills_field"] = "skills" in response
            
            skills = response.get("skills", [])
            validation["skills_is_list"] = isinstance(skills, list)
            validation["skills_count"] = len(skills)
            
            if skills:
                first_skill = skills[0]
                validation["skill_has_id"] = "id" in first_skill
                validation["skill_has_name"] = "name" in first_skill
                validation["skill_has_description"] = "description" in first_skill
                validation["skill_has_type"] = "type" in first_skill
                validation["skill_has_trigger_phrases"] = "trigger_phrases" in first_skill
                
                # Check for builtin skills
                skill_names = [s.get("name", "").lower() for s in skills]
                validation["has_weather_skill"] = "weather" in skill_names
                validation["has_calculator_skill"] = "calculator" in skill_names
                validation["has_notes_skill"] = "notes" in skill_names
            
            is_valid = (response.get("success") is True and 
                       isinstance(skills, list) and
                       len(skills) > 0)
            
            self.log_detailed_test("Skills List Detailed", is_valid, response, validation)
        else:
            self.log_detailed_test("Skills List Detailed", False, response, {"error": "Skills request failed"})

    def test_integrations_detailed(self):
        """Detailed test of integrations endpoint"""
        if not self.token:
            self.log_detailed_test("Integrations Detailed", False, {}, {"error": "No auth token"})
            return
            
        success, response = self.make_request('GET', '/api/integrations')
        
        validation = {}
        if success:
            validation["has_success_field"] = "success" in response
            validation["has_integrations_field"] = "integrations" in response
            
            integrations = response.get("integrations", [])
            validation["integrations_is_list"] = isinstance(integrations, list)
            validation["integrations_count"] = len(integrations)
            
            if integrations:
                first_integration = integrations[0]
                validation["integration_has_id"] = "id" in first_integration
                validation["integration_has_name"] = "name" in first_integration
                validation["integration_has_status"] = "status" in first_integration
                
                # Check for expected integrations
                integration_ids = [i.get("id", "") for i in integrations]
                expected_integrations = ["telegram", "gmail", "calendar", "notion", "github", "gemini"]
                validation["has_expected_integrations"] = all(exp in integration_ids for exp in expected_integrations)
                validation["integration_ids"] = integration_ids
            
            is_valid = (response.get("success") is True and 
                       isinstance(integrations, list) and
                       len(integrations) >= 6)  # Should have at least 6 integrations
            
            self.log_detailed_test("Integrations Detailed", is_valid, response, validation)
        else:
            self.log_detailed_test("Integrations Detailed", False, response, {"error": "Integrations request failed"})

    def test_desktop_status_detailed(self):
        """Detailed test of desktop status endpoint"""
        if not self.token:
            self.log_detailed_test("Desktop Status Detailed", False, {}, {"error": "No auth token"})
            return
            
        success, response = self.make_request('GET', '/api/desktop/status')
        
        validation = {}
        if success:
            validation["has_success_field"] = "success" in response
            validation["has_status_field"] = "status" in response
            validation["has_agent_info_field"] = "agent_info" in response
            
            status = response.get("status")
            agent_info = response.get("agent_info")
            
            validation["status_value"] = status
            validation["status_is_valid"] = status in ["connected", "offline"]
            validation["agent_info_type"] = type(agent_info).__name__
            
            # Desktop agent is expected to be offline in test environment
            is_valid = (response.get("success") is True and 
                       status in ["connected", "offline"])
            
            self.log_detailed_test("Desktop Status Detailed", is_valid, response, validation)
        else:
            self.log_detailed_test("Desktop Status Detailed", False, response, {"error": "Desktop status request failed"})

    def run_detailed_tests(self):
        """Run all detailed API tests"""
        print("🔍 Starting Detailed OpenClaw API Testing...")
        print(f"📍 Base URL: {self.base_url}")
        print(f"👤 Test User: {self.test_email}")
        print("=" * 70)
        
        # Test health endpoint
        self.test_health_detailed()
        
        # Test login and get tokens
        login_success = self.test_login_detailed()
        
        if login_success:
            # Test authenticated endpoints with detailed validation
            self.test_user_profile_detailed()
            self.test_command_processing_detailed()
            self.test_skills_detailed()
            self.test_integrations_detailed()
            self.test_desktop_status_detailed()
        else:
            print("⚠️  Skipping authenticated endpoint tests due to login failure")
        
        # Print detailed summary
        print("=" * 70)
        print(f"📊 Detailed Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        # Print any failed tests
        failed_tests = [r for r in self.detailed_results if not r["success"]]
        if failed_tests:
            print("\n❌ Failed Tests:")
            for test in failed_tests:
                print(f"   - {test['test_name']}")
                if test.get("validation_details", {}).get("error"):
                    print(f"     Error: {test['validation_details']['error']}")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All detailed tests passed!")
            return 0
        else:
            print("❌ Some detailed tests failed.")
            return 1

def main():
    """Main detailed test execution"""
    tester = DetailedAPITester()
    return tester.run_detailed_tests()

if __name__ == "__main__":
    sys.exit(main())